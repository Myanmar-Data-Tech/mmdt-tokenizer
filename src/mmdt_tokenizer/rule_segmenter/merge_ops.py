from typing import List
from .types import Chunk
from .lexicon import FUN_TAG

def noun_classifier(chunks: List[Chunk]) -> List[Chunk]:
    out: List[Chunk] = []
    i = 0
    n = len(chunks)


    return out

def merge_day_classifier(chunks: List[Chunk]) -> List[Chunk]:
    out: List[Chunk] = []
    i = 0
    n = len(chunks)
    while i <n:
        if chunks[i].tag == "DAY":
            j = i
            has_right_cl = False
            while j<n and  chunks[j].tag in ("DAY", "CL", "PUNCT"): 
                if chunks[j].text in ("နေ့", "ရက်"): has_right_cl = True
                j +=1
            start = chunks[i].span[0]
            end = chunks[min(n,j-1)].span[1]
            merged_text = "".join(c.text for c in chunks[i:j])
            merged_text = merged_text.strip().replace(" ", "")
            
            if (j<n) and has_right_cl:
                out.append(Chunk((start, end), merged_text, "DAYCL"))
                i = j 
                continue

            out.append(Chunk((start, end), merged_text, "DAY"))
            i = j
            continue
        
        out.append(chunks[i])
        i += 1
    return out

def merge_num_classifier(chunks: List[Chunk]) -> List[Chunk]:
    out: List[Chunk] = []
    i = 0
    n = len(chunks)
    NUMBER_TAGS = ("NUM", "WORDNUM")
    
    while i< n: 
        if chunks[i].tag in NUMBER_TAGS:
            if chunks[i].text == "ရာခိုင်နှုန်း":
                out.append(Chunk(chunks[i].span, chunks[i].text, "NUMCL"))
                i += 1
                continue
            j = i
            start = chunks[i].span[0]

            while j < n and (chunks[j].tag in NUMBER_TAGS or chunks[j].tag =="PUNCT"):
                j += 1

            merged_text = "".join(c.text for c in chunks[i:j])
            merged_text = merged_text.strip().replace(" ","")
            end = chunks[j-1].span[1]

            if j< n and chunks[j].tag in ("CL", "WORDNUM", "CLEP"):
                cls_chunk = chunks[j]
                num_cls_text = merged_text + cls_chunk.text
                out.append(Chunk((start, chunks[j].span[1]), num_cls_text, "NUMCL"))
                i = j + 1
                continue

            seg = chunks[i:j]
            if(len(seg)==1 and seg[0].tag =="WORDNUM"): final_tag = "WORDNUM"
            else: final_tag = "NUM"

            out.append(Chunk((start, end), merged_text, final_tag))
    
            i = j
            continue

        out.append(chunks[i])
        i += 1
        
    return out

def merge_predicate(chunks: List["Chunk"]) -> List["Chunk"]:
    n = len(chunks)
    i = n - 1
    out = []
    
    neg_sent_sfp = ("ပါ", "ဘူး", "နဲ့")
    que_sent_sfp = ("နည်း", 'လား', 'လဲ', 'တုံး')
    while i >= 0:
        if(chunks[i].tag in FUN_TAG):
            out.append(chunks[i])
            i-=1
            continue
        if chunks[i].tag == "SFP":
            j = i
            raw_indexs = []
            neg_index = None
            que_index = None
            while j >= 0 and chunks[j].tag in ("SFP", "VEP", "RAW", "QW"): 
                if chunks[j].tag == "RAW": raw_indexs.append(j)
                if chunks[j].text == "မ" and neg_index is None: neg_index = j
                if chunks[j].tag == "QW" and que_index is None: que_index = j
                j -= 1
            pred_length = i - j
            if pred_length > 1 :
                start = chunks[j + 1].span[0]
                end = chunks[i].span[1]
                text = "".join(ch.text for ch in chunks[j + 1 : i + 1])
                if neg_index is not None and chunks[i].text in neg_sent_sfp: 
                    text = "".join(ch.text for ch in chunks[neg_index : i + 1])           
                    out.append(Chunk((neg_index, end), text, "PRED"))
                    text = "".join(ch.text for ch in chunks[j + 1 : neg_index])
                    out.append(Chunk((start, neg_index), text, "RAW"))
                elif que_index is not None and chunks[i].text in que_sent_sfp: 
                    text = "".join(ch.text for ch in chunks[que_index : i + 1])           
                    out.append(Chunk((que_index, end), text, "PRED"))
                    text = "".join(ch.text for ch in chunks[j + 1 : que_index])
                    out.append(Chunk((start, que_index), text, "RAW"))
                elif len(raw_indexs)>0:
                    raw_index = raw_indexs[0]
                    text = "".join(ch.text for ch in chunks[raw_index+1 : i + 1])        
                    out.append(Chunk((raw_index, end), text, "PRED"))
                    text = "".join(ch.text for ch in chunks[j + 1 : raw_index + 1])
                    out.append(Chunk((start, raw_index), text, "PVERB"))
                else:
                    out.append(Chunk((start, end), text, "PRED"))
                
                i = j
                continue            
        out.append(chunks[i])
        i -= 1

    return out[::-1]