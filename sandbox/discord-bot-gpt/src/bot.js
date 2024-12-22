const { Client, GatewayIntentBits } = require('discord.js');
const config = require('../config/config.json');

const client = new Client({ intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMessages, GatewayIntentBits.MessageContent] });

client.once('ready', () => {
    console.log(`Logged in as ${client.user.tag}!`);
});

client.on('messageCreate', async message => {
    if (message.author.bot) return;
    
    if (message.content.startsWith('!gpt')) {
        const prompt = message.content.replace('!gpt', '').trim();
        const response = `You said: ${prompt}`; // Replace with GPT integration
        message.reply(response);
    }
});

client.login(config.token);