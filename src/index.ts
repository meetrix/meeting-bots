import express from 'express';
import { joinGoogleMeet } from './joinGoogleMeet';
import { JoinGoogleMeetParams } from './types';

const app = express();
const port = 3000;

app.use(express.json());

app.post('/join-meet', async (req, res) => {
  const { googleMeetUrl, fullName, message } = req.body as JoinGoogleMeetParams;
  if (!googleMeetUrl || !fullName || !message) {
    return res.status(400).send('Missing required parameters');
  }

  try {
    await joinGoogleMeet({ googleMeetUrl, fullName, message });
    res.status(200).send('Joined Google Meet and sent message successfully');
  } catch (error) {
    console.error('Error joining Google Meet:', error);
    res.status(500).send('Failed to join Google Meet');
  }
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
