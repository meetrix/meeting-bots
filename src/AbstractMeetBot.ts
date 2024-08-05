// src/AbstractMeetBot.ts
export interface JoinParams {
  url: string;
  fullName: string;
  fakeVideoPath?: string; // Optional property for fake video path
}

export interface SendChatMessageParams {
  message: string;
  pinMessage?: boolean; // Optional property for pinning the message
}

export abstract class AbstractMeetBot {
  abstract join(params: JoinParams): Promise<void>;
  abstract sendChatMessage(params: SendChatMessageParams): Promise<void>;
}
