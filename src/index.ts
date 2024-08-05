// src/index.ts
import express from 'express';
import { GoogleMeetBot } from './GoogleMeetBot';
import { JoinParams, SendChatMessageParams } from './AbstractMeetBot';

const app = express();
const port = 3000;

app.use(express.json());

app.post('/join-meet', async (req, res) => {
  const { url, fullName, message, pinMessage, fakeVideoPath } = req.body as JoinParams & SendChatMessageParams;
  if (!url || !fullName || !message) {
    return res.status(400).send('Missing required parameters');
  }

  try {
    const bot = new GoogleMeetBot();
    await bot.join({ url, fullName, fakeVideoPath });
    await bot.sendChatMessage({ message, pinMessage });
    res.status(200).send('Joined Google Meet and sent message successfully');
  } catch (error) {
    console.error('Error joining Google Meet:', error);
    res.status(500).send('Failed to join Google Meet');
  }
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
