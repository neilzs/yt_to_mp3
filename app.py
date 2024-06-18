import streamlit as st
from pytube import YouTube
from pydub import AudioSegment
import os

def download_youtube_video_as_mp3(url, output_path, bitrate="320k"):
    yt = YouTube(url)
    video = yt.streams.filter(only_audio=True).first()
    downloaded_file = video.download(output_path=output_path)
    base, ext = os.path.splitext(downloaded_file)
    new_file = base + '.mp3'
    audio = AudioSegment.from_file(downloaded_file)
    audio.export(new_file, format="mp3", bitrate=bitrate)
    os.remove(downloaded_file)
    return new_file

def run():
    st.title("YouTube to MP3 Converter")
    st.write("Masukkan URL video YouTube untuk mengunduh dan mengonversinya menjadi MP3 dengan bitrate 320kbps.")
    youtube_url = st.text_input("YouTube URL")
    output_directory = "./downloads"
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    if st.button("Download and Convert"):
        if youtube_url:
            with st.spinner("Mengunduh dan mengonversi..."):
                try:
                    mp3_file = download_youtube_video_as_mp3(youtube_url, output_directory)
                    st.success("Berhasil mengunduh dan mengonversi! Anda dapat mengunduh file MP3 di bawah ini.")
                    with open(mp3_file, "rb") as file:
                        btn = st.download_button(label="Download MP3", data=file, file_name=os.path.basename(mp3_file), mime="audio/mp3")
                except Exception as e:
                    st.error(f"Terjadi kesalahan: {e}")
        else:
            st.error("Harap masukkan URL YouTube yang valid.")

if __name__ == "__main__":
    run()
