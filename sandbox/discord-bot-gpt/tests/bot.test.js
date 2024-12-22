const { Client, GatewayIntentBits } = require('discord.js');
const config = require('../config/config.json');

jest.mock('discord.js', () => {
    const mockClient = {
        once: jest.fn(),
        on: jest.fn(),
        login: jest.fn().mockResolvedValue('Mocked Token')
    };
    return {
        Client: jest.fn(() => mockClient),
        GatewayIntentBits: { Guilds: 1, GuildMessages: 2, MessageContent: 3 }
    };
});

describe('Discord Bot', () => {
    let client;

    beforeEach(() => {
        client = new Client({ intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMessages, GatewayIntentBits.MessageContent] });
    });

    test('should log in successfully', async () => {
        await client.login(config.token);
        expect(client.login).toHaveBeenCalledWith(config.token);
    });

    test('should respond to !gpt command', () => {
        const message = {
            author: { bot: false },
            content: '!gpt Test message',
            reply: jest.fn()
        };

        const bot = require('../src/bot'); // Load bot to attach events
        const messageHandler = client.on.mock.calls.find(call => call[0] === 'messageCreate')[1];

        messageHandler(message);
        expect(message.reply).toHaveBeenCalledWith('You said: Test message');
    });
});