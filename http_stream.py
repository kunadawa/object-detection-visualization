import imageio
import os
import imageio_ffmpeg

def write_video_to_stream(path_to_video, rtp_port):
    video_reader = imageio.get_reader(path_to_video)
    print(video_reader.get_meta_data())
    rtp_url = f"http://localhost:{rtp_port}"
    output_params = [ '-f', 'webm', '-listen', "1", '-seekable', '0',
        '-headers', 'Access-Control-Allow-Origin: http://localhost:3000\r\n']
    input_params = ['-re']
    img_writer = imageio_ffmpeg.write_frames(
            rtp_url,
            size=video_reader.get_meta_data()['size'],
            output_params=output_params,
            input_params=input_params,
            codec='vp9',
    )
    img_writer.send(None)
    for frame in video_reader:
        #try:
            img_writer.send(frame)
        #except KeyboardInterrupt as e:
        #    print(e)
        #    img_writer.close()
        #    break
    img_writer.close()

# python http_stream.py "<video0>" 50644
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("path_to_video")
    parser.add_argument("rtp_port")
    ns = parser.parse_args()
    write_video_to_stream(ns.path_to_video, ns.rtp_port)
