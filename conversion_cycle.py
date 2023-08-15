from pydub import AudioSegment
from random import randint
from shutil import copy as clone
from glob import glob
from os import remove as delete

formats = ["wav", "mp3", "ogg", "flac", "aiff", "flv", "asf", "ast", "avi", "webm", "NUT"]

def ccycle(numConversions: int, fp: str, bf: str = None):
    if '.' in fp:
        if bf is None:     filename, baseFormat = fp[:fp.rfind('.')], fp[fp.rfind('.') + 1:]
        elif bf not in fp: raise ValueError("File formats conflict")
        else:              filename, baseFormat = fp[:fp.rfind('.')], bf
    else: filename, baseFormat = fp, bf
    
    print(f"Performing conversions of {filename}.{baseFormat} ...")

    newName = f"{filename} +mash-{numConversions}"

    format = baseFormat
    clone(src=f"{filename}.{baseFormat}", dst=f"{newName}.{format}")
    for c in range(0, numConversions):
        if c % 10 == 0: print(f"{c} conversions complete.")
        data = AudioSegment.from_file(f"{newName}.{format}", format=format)
        format = formats[randint(0, len(formats) - 1)]
        data.export(f"{newName}.{format}", format=format)

    print(f"{numConversions} conversions complete. Cleaning up...")
    data = AudioSegment.from_file(f"{newName}.{format}", format=format)
    for path in glob(f"{newName}.*"):
        delete(path)
    data.export(f"{newName}.{baseFormat}", format=baseFormat)
        
# ccycle(100, "Aresult.wav")