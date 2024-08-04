// src/AbstractMeetBot.ts
export interface JoinParams {
  url: string;
  fullName: string;
}

export interface SendChatMessageParams {
  message: string;
  pin: boolean;
}

export abstract class AbstractMeetBot {
  abstract join(params: JoinParams): Promise<void>;
  abstract sendChatMessage(params: SendChatMessageParams): Promise<void>;
}
