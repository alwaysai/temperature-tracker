import time
import edgeiq
from temperature_tracker import TemperatureTracker

"""
Use object detection to detect objects in the frame in realtime. The
types of objects detected can be changed by selecting different models.

To change the computer vision model, follow this guide:
https://dashboard.alwaysai.co/docs/application_development/changing_the_model.html

To change the engine and accelerator, follow this guide:
https://dashboard.alwaysai.co/docs/application_development/changing_the_engine_and_accelerator.html
"""


def main():

    obj_detect = edgeiq.ObjectDetection(
            "alwaysai/mobilenet_ssd")
    obj_detect.load(engine=edgeiq.Engine.DNN)

    print("Loaded model:\n{}\n".format(obj_detect.model_id))
    print("Engine: {}".format(obj_detect.engine))
    print("Accelerator: {}\n".format(obj_detect.accelerator))
    print("Labels:\n{}\n".format(obj_detect.labels))

    temperature_tracker = TemperatureTracker()

    fps = edgeiq.FPS()

    try:
        with edgeiq.WebcamVideoStream(cam=0) as video_stream, \
                edgeiq.Streamer() as streamer:
            
            # Allow Webcam to warm up
            time.sleep(2.0)
            fps.start()

            # start the temperature tracker
            temperature_tracker.start()

            # loop detection
            while True:
                frame = video_stream.read()
                results = obj_detect.detect_objects(frame, confidence_level=.5)
                frame = edgeiq.markup_image(
                        frame, results.predictions, colors=obj_detect.colors)

                # Generate text to display on streamer
                text = ["Model: {}".format(obj_detect.model_id)]
                text.append(
                        "Inference time: {:1.3f} s".format(results.duration))
                text.append("Objects:")

                for prediction in results.predictions:
                    text.append("{}: {:2.2f}%".format(
                        prediction.label, prediction.confidence * 100))

                # blank line for readability
                text.append("")

                # get an instance of the cpu temperature
                temperature_tracker.update()

                # gather the current temperature and timestamp and print it
                now = temperature_tracker.now()

                # log block showing current temperature
                text.append("{:1.2f}C/{:1.2f}F at time {}\n".format(now[0], ((now[0]*(9 / 5)) + 32),time.strftime('%Y-%m-%d %H:%M:%S', now[1])))

                # details whether the temperature is safe for a Raspberry Pi 4
                if now[0] < temperature_tracker.MAX_TEMP_RASP4:
                    text.append("Temperature is safe")
                else:
                    text.append("TEMPERATURE IS NO LONGER SAFE")


                streamer.send_data(frame, text)

                fps.update()


                # exit program if maximum safe temp has been reached
                if now[0] >= temperature_tracker.MAX_TEMP_RASP4:
                    print("MAXIMUM SAFE TEMPERATURE REACHED. Powering down application.")
                    break


                if streamer.check_exit():
                    break

    finally:
        fps.stop()

        # stop the temperature tracker
        temperature_tracker.stop()

        # print summary details for inference time
        print("elapsed time: {:.2f}".format(fps.get_elapsed_seconds()))
        print("approx. FPS: {:.2f}".format(fps.compute_fps()))
        
        # print summary details for the temperature tracker
        summary = temperature_tracker.summary()
        print(summary)

        print("Program Ending")


if __name__ == "__main__":
    main()
