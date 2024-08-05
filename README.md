# Google Meet Bot

A bot that can join google meet with following capabilities

1. Showing a dummy video
2. Sending a message

Built with playwright-extra

## Usage

1. `npm i`
2. `npm start`
3. Run following command on a separate terminal to join a meeting

   ```bash
   curl -X POST http://localhost:3000/join-meet \
   -H "Content-Type: application/json" \
   -d '{
   "url": "https://meet.google.com/ynw-zmcg-qfq",
   "fullName": "Buddhika",
   "message": "this is a test message",
   "fakeVideoPath": "/absolute/path/to/your/video.y4m",
   "pinMessage": true
   }'

   ```

### Usage with docker

1. `docker compose up`
2. `docker-compose exec -it google-meet-bot /bin/bash`
3. `xvfb-run --auto-servernum --server-args='-screen 0 1280x720x24' npm start`
4. Then run the curl command step 3 above

## Other commands

### Generating a video from an image

1. `ffmpeg -loop 1 -i ./assets/images/sample.png -pix_fmt yuv420p -t 0.05 ./assets/videos/sample.y4m`

## LICENSE

MIT
