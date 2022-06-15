FROM ubuntu
RUN mkdir /gif_script
COPY script.sh /gif_script
WORKDIR /gif_script
RUN apt-get update && apt-get install -y ffmpeg

ENTRYPOINT [ "./script.sh" ]