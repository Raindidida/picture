const fs = require('fs');
const path = require('path');

function readWavAsFloat32(filePath) {
  const buf = fs.readFileSync(filePath);
  if (buf.toString('ascii', 0, 4) !== 'RIFF' || buf.toString('ascii', 8, 12) !== 'WAVE') {
    throw new Error('Unsupported WAV file');
  }

  let offset = 12;
  let audioFormat;
  let numChannels;
  let sampleRate;
  let bitsPerSample;
  let dataOffset;
  let dataSize;

  while (offset + 8 <= buf.length) {
    const chunkId = buf.toString('ascii', offset, offset + 4);
    const chunkSize = buf.readUInt32LE(offset + 4);
    const chunkData = offset + 8;

    if (chunkId === 'fmt ') {
      audioFormat = buf.readUInt16LE(chunkData);
      numChannels = buf.readUInt16LE(chunkData + 2);
      sampleRate = buf.readUInt32LE(chunkData + 4);
      bitsPerSample = buf.readUInt16LE(chunkData + 14);
    } else if (chunkId === 'data') {
      dataOffset = chunkData;
      dataSize = chunkSize;
      break;
    }

    offset = chunkData + chunkSize + (chunkSize % 2);
  }

  if (audioFormat !== 1 || numChannels !== 1 || bitsPerSample !== 16 || !dataOffset) {
    throw new Error(`Expected PCM16 mono WAV, got format=${audioFormat} channels=${numChannels} bits=${bitsPerSample}`);
  }

  const sampleCount = dataSize / 2;
  const audio = new Float32Array(sampleCount);
  for (let i = 0; i < sampleCount; i++) {
    audio[i] = buf.readInt16LE(dataOffset + i * 2) / 32768;
  }

  return { audio, sampleRate };
}

function formatTime(seconds) {
  if (seconds == null || Number.isNaN(seconds)) return '??:??';
  const total = Math.max(0, Math.round(seconds));
  const mm = String(Math.floor(total / 60)).padStart(2, '0');
  const ss = String(total % 60).padStart(2, '0');
  return `${mm}:${ss}`;
}

async function main() {
  const inputWav = process.argv[2];
  const outputTxt = process.argv[3];
  const outputJson = process.argv[4];

  if (!inputWav || !outputTxt || !outputJson) {
    throw new Error('Usage: node transcribe_whisper_local.js <inputWav> <outputTxt> <outputJson>');
  }

  const { pipeline, env } = await import('file:///E:/picture2/node_modules/@xenova/transformers/src/transformers.js');
  env.cacheDir = 'E:/picture2/.cache';
  env.localModelPath = 'E:/picture2/models/';
  env.allowRemoteModels = false;

  const transcriber = await pipeline(
    'automatic-speech-recognition',
    'Xenova/whisper-tiny',
    { local_files_only: true }
  );

  const { audio, sampleRate } = readWavAsFloat32(inputWav);
  const result = await transcriber(audio, {
    chunk_length_s: 30,
    stride_length_s: 5,
    language: 'en',
    return_timestamps: true,
    sampling_rate: sampleRate,
  });

  const lines = [];
  lines.push('全文整理');
  lines.push('');
  lines.push((result.text || '').trim());
  lines.push('');
  lines.push('分段时间轴');
  lines.push('');

  for (const chunk of result.chunks || []) {
    const start = formatTime(chunk.timestamp?.[0]);
    const end = formatTime(chunk.timestamp?.[1]);
    lines.push(`[${start}-${end}] ${(chunk.text || '').trim()}`);
  }

  fs.mkdirSync(path.dirname(outputTxt), { recursive: true });
  fs.writeFileSync(outputTxt, lines.join('\n'), 'utf8');
  fs.writeFileSync(outputJson, JSON.stringify(result, null, 2), 'utf8');
  process.stdout.write(`Saved: ${outputTxt}\nSaved: ${outputJson}\n`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
