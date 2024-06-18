import streamlit as st
from pytube import YouTube
from pydub import AudioSegment
import os
import re
import threading

# Function to sanitize file name
def sanitize_filename(filename):
    # Replace invalid characters with underscores
    return re.sub(r'[\\/*?:"<>|\s-]', '_', filename)

# Function to download YouTube video audio and convert to specified format
def download_and_convert(url, output_path, audio_format="mp3", bitrate="320k"):
    try:
        yt = YouTube(url)
        title = sanitize_filename(yt.title)
        video = yt.streams.filter(only_audio=True).first()
        downloaded_file = video.download(output_path=output_path, filename=title)

        base, ext = os.path.splitext(downloaded_file)
        new_file = f"{base}.{audio_format}"

        audio = AudioSegment.from_file(downloaded_file)
        audio.export(new_file, format=audio_format, bitrate=bitrate)

        os.remove(downloaded_file)
        return new_file
    except Exception as e:
        raise Exception(f"Gagal mengunduh atau mengonversi: {e}")

# Function to run Streamlit app
def run():
    st.title("YouTube Audio Downloader")
    st.write("Masukkan URL video YouTube untuk mengunduh dan mengonversinya menjadi format audio pilihan Anda.")
    youtube_url = st.text_input("URL YouTube")
    audio_format = st.radio("Pilih Format Audio", ("MP3", "FLAC", "WAV"))
    output_directory = "./downloads"

    if st.button("Convert") and youtube_url:
        try:
            bitrate = "320k" if audio_format == "MP3" else None
            with st.spinner("Sedang mengkonversi..."):
                audio_file = download_and_convert(youtube_url, output_directory, audio_format.lower(), bitrate)
                st.success(f"Berhasil mengkonversi ke format {audio_format.upper()}! Anda dapat mengunduh file di bawah ini.")
                with open(audio_file, "rb") as file:
                    st.download_button(label=f"Download {audio_format.upper()}", data=file, file_name=os.path.basename(audio_file), mime=f"audio/{audio_format.lower()}")
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")

if __name__ == "__main__":
    run()
