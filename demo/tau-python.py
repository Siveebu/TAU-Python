import soundfile as sf
import pyworld as pw
import numpy as np
#import os

sampleRate = 44100

class Note:
    def __init__(self, midiPitch, startTime, endTime):
        self.midiPitch = midiPitch
        self.startTimeMilliseconds = startTime
        self.endTimeMilliseconds = endTime

def midiNoteToHz(midiNote):
    return 440 * 2**((midiNote-69)/12)

def renderNote(note):
    sampleArray, sampleRate = sf.read("demo/test_audio/nya.wav")
    f0, t = pw.harvest(sampleArray, sampleRate, pw.default_f0_floor, f0_ceil=1760)
    sp = pw.cheaptrick(sampleArray, f0, t, sampleRate)
    ap = pw.d4c(sampleArray, f0, t, sampleRate)

    pitchArray = f0
    pitchArray.fill(midiNoteToHz(note))
    renderedNote = pw.synthesize(pitchArray, sp, ap, sampleRate, pw.default_frame_period)
    return renderedNote

def msToSamples(milliseconds):
    samples = milliseconds * sampleRate / 1000
    return samples

def renderNotesWithTiming(notes):
    renderedNotes = [renderNote(note.midiPitch) for note in notes]
    result = np.empty(int(msToSamples(notes[-1].endTimeMilliseconds)))
    for index, render in enumerate(renderedNotes):
        startTimeSamples = msToSamples(notes[index].startTimeMilliseconds)
        sampleIndices = np.arange(startTimeSamples, startTimeSamples+len(render))
        np.put(result, sampleIndices.astype(int), render)
    return result
   
def createSequentialNotes (pitches, noteLengthMS):
    notes = []
    currentTime = 0
    for pitch in pitches:
        notes.append(Note(pitch, currentTime, currentTime + noteLengthMS))
        currentTime += noteLengthMS
    return notes

def main():
    notes = createSequentialNotes([60, 62, 64, 65, 67, 69, 71, 72], 600)
    render = renderNotesWithTiming(notes)
    sf.write("demo/demo.wav", render, sampleRate)

main()
