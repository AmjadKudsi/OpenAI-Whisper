import subprocess
import math
import os
import tempfile
import time
from openai import OpenAI


class MediaProcessorService:
    def __init__(self):
        self.client = OpenAI()

    def summarize_transcription(self, text):
        """Generate a concise summary of the transcription"""

        # TODO: complete the implementation of this summarization method via OpenAI API
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an expert content analyst and summarizer with these capabilities:\n"
                            "- Extracting key points while maintaining context\n"
                            "- Identifying main themes and core messages\n"
                            "- Preserving critical details while reducing length\n"
                            "- Maintaining the original tone and intent\n"
                            "- Organizing information hierarchically\n\n"
                            "Format your summaries with:\n"
                            "1. A one-sentence overview\n"
                            "2. 2-3 key takeaways\n"
                            "3. Important details or quotes (if any)"
                        )
                    },
                    {
                        "role": "user",
                        "content": (
                            f"Create a structured summary of this transcription. "
                            f"Focus on the core message and key points while maintaining "
                            f"context and critical details.\n\n"
                            f"Transcription:\n{text}"
                        )
                    }
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating summary: {e}")
            return None

    def run_command_with_output(self, cmd, desc=None):
        """Run a command and stream its output in real-time"""
        if desc:
            print(f"\n{desc}")
        
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        output = []
        for line in iter(process.stdout.readline, ''):
            print(line, end='')
            output.append(line)
        
        process.stdout.close()
        return_code = process.wait()
        
        if return_code != 0:
            raise subprocess.CalledProcessError(return_code, cmd)
        
        return ''.join(output)

    def get_audio_duration(self, file_path):
        """Get the duration of an audio file using ffprobe"""
        cmd = [
            'ffprobe', 
            '-v', 'quiet',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            file_path
        ]
        try:
            output = subprocess.check_output(cmd)
            return float(output)
        except Exception:
            return None

    def split_audio(self, file_path, chunk_size_mb=20):
        """Split audio file into chunks smaller than the API limit"""
        print("\nSplitting audio into chunks...")
        
        MAX_CHUNK_SIZE = 25 * 1024 * 1024  # 25MB in bytes
        MAX_MEDIA_DURATION_SECONDS = 40 * 60  # 40 minutes
        file_size = os.path.getsize(file_path)
        duration = self.get_audio_duration(file_path)
        
        if not duration:
            raise Exception("Could not determine audio duration")
            
        if duration > MAX_MEDIA_DURATION_SECONDS:
            raise Exception(
                "Sorry, your video is too long."
                "To avoid extensive waiting times,"
                "for this demo application we're only transcribing videos up to 40 minutes long"
            )
        
        chunk_duration = duration * (chunk_size_mb * 1024 * 1024) / file_size
        num_chunks = math.ceil(duration / chunk_duration)
        chunks = []
        
        for current_chunk in range(num_chunks):
            start_time = current_chunk * chunk_duration
            original_ext = os.path.splitext(file_path)[1]
            
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=original_ext)
            temp_file_path = temp_file.name
            temp_file.close()
            
            cmd = [
                'ffmpeg',
                '-i', file_path,
                '-ss', str(start_time),
                '-t', str(chunk_duration),
                '-c', 'copy',
                '-y',
                temp_file_path
            ]
            
            self.run_command_with_output(cmd, f"Extracting chunk {current_chunk+1}/{num_chunks}:")
            time.sleep(0.5)
            
            chunk_size = os.path.getsize(temp_file_path)
            if chunk_size > MAX_CHUNK_SIZE:
                print(f"Chunk {current_chunk+1} too large ({chunk_size/1024/1024:.1f}MB), reducing duration...")
                try:
                    os.unlink(temp_file_path)
                except Exception as e:
                    print(f"Warning: Could not delete oversized chunk: {e}")
                chunk_duration *= 0.8
                num_chunks = math.ceil(duration / chunk_duration)
                continue
            
            chunks.append(temp_file_path)
        
        return chunks

    def transcribe_audio(self, audio_file):
        """Transcribe an audio file to text, handling files larger than the API limit"""
        try:
            file_size = os.path.getsize(audio_file)
            max_size = 5 * 1024 * 1024  # 5MB in bytes
            
            if file_size > max_size:
                print(f"\nFile size ({file_size / 1024 / 1024:.2f}MB) exceeds API limit. Splitting into chunks...")
                chunks = self.split_audio(audio_file)
                
                if not chunks:
                    raise Exception("Failed to split audio file into chunks")
                    
                full_transcription = []
                
                for i, chunk_path in enumerate(chunks, 1):
                    max_retries = 3
                    retry_count = 0
                    
                    while retry_count < max_retries:
                        try:
                            print(f"\nTranscribing chunk {i} of {len(chunks)}...")
                            with open(chunk_path, "rb") as audio_file:
                                response = self.client.audio.transcriptions.create(
                                    model="whisper-1",
                                    file=audio_file,
                                    timeout=60
                                )
                                full_transcription.append(response.text)
                                break
                        except Exception as e:
                            retry_count += 1
                            print(f"Error on chunk {i} (attempt {retry_count}): {str(e)}")
                            if retry_count == max_retries:
                                print(f"Failed to transcribe chunk {i} after {max_retries} attempts")
                                raise
                            print(f"Retrying in 5 seconds...")
                            time.sleep(5)
                    
                    try:
                        os.unlink(chunk_path)
                    except Exception as e:
                        print(f"Warning: Could not delete temporary file {chunk_path}: {e}")
                
                return ' '.join(full_transcription)
            else:
                print("\nTranscribing audio...")
                with open(audio_file, "rb") as audio_file:
                    response = self.client.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_file,
                        timeout=60
                    )
                    return response.text
        except Exception as e:
            print(f"Error during transcription: {e}")
            print(f"Error type: {type(e)}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            return None

    def cleanup_temp_files(self, file_path):
        """Clean up temporary files and directories"""
        try:
            if os.path.isfile(file_path):
                for _ in range(5):  # Try up to 5 times
                    try:
                        os.unlink(file_path)
                        break
                    except PermissionError:
                        time.sleep(1)
                    except Exception as e:
                        print(f"Warning: Could not clean up {file_path}: {e}")
                        break
            elif os.path.isdir(file_path):
                for root, dirs, files in os.walk(file_path, topdown=False):
                    for name in files:
                        try:
                            os.unlink(os.path.join(root, name))
                        except Exception as e:
                            print(f"Warning: Could not clean up file {name}: {e}")
                    for name in dirs:
                        try:
                            os.rmdir(os.path.join(root, name))
                        except Exception as e:
                            print(f"Warning: Could not clean up directory {name}: {e}")
                try:
                    os.rmdir(file_path)
                except Exception as e:
                    print(f"Warning: Could not clean up directory {file_path}: {e}")
        except Exception as e:
            print(f"Warning: Could not clean up {file_path}: {e}")