from typing import List
from .types import Chunk
from .lexicon import FUN_TAG


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
    while i < n:
        if chunks[i].tag == "NUM":
            j = i
            start = chunks[i].span[0]

            while j < n and chunks[j].tag in ("NUM", "PUNCT"):
                j += 1
                       
            merged_text = "".join(c.text for c in chunks[i:j])
            merged_text = merged_text.strip().replace(" ","")
            end = chunks[j-1].span[1]

            # Number followed by classifier
            if j< n and chunks[j].tag in ("CL", "WORDNUM"):
                out.append(Chunk((start, chunks[j].span[1]), merged_text + chunks[j].text, "NUMCL"))
                i = j + 1
                continue
            
            # multi-token or solitary digit number
            out.append(Chunk((start, end), merged_text, "NUM"))
            i = j
            continue
        elif chunks[i].tag == "WORDNUM":
            j = i
            while j < n and chunks[j].tag in ("WORDNUM", "PUNCT"):
                j += 1

            merged_text = "".join(c.text for c in chunks[i:j]).replace(" ", "")
            start, end = chunks[i].span[0], chunks[j - 1].span[1]

            # If followed by a classifier → NUMCL
            if j < n and chunks[j].tag == "CL":
                num_cls_text = merged_text + chunks[j].text
                out.append(Chunk((start, chunks[j].span[1]), num_cls_text, "WNUMCL"))
                i = j + 1
                continue

            # Multi-word number → NUM
            out.append(Chunk((start, end), merged_text, "WORDNUM"))
            i = j
            continue
        # the rest
        out.append(chunks[i])
        i += 1
    return out

def merge_predicate(chunks: List["Chunk"]) -> List["Chunk"]:
    n = len(chunks)
    i = n - 1
    out = []
    max_phrase_length = 5
    while i >= 0:
        if(chunks[i].tag in FUN_TAG):
            out.append(chunks[i])
            i-=1
            continue
        if chunks[i].tag == "SFP":
            j = i
            raw_indexs = []
            neg_index = None
            while j >= 0 and chunks[j].tag in ("SFP", "VEP", "RAW"): 
                if chunks[j].tag == "RAW": raw_indexs.append(j)
                if chunks[j].text == "မ" and neg_index is None: neg_index = j
                j -= 1
            pred_length = i - j
            if pred_length > 1 :
                start = chunks[j + 1].span[0]
                end = chunks[i].span[1]
                text = "".join(ch.text for ch in chunks[j + 1 : i + 1])
                if neg_index is not None and chunks[i].text in ("ပါ", "ဘူး", "နဲ့"): 
                    text = "".join(ch.text for ch in chunks[neg_index : i + 1])           
                    out.append(Chunk((neg_index, end), text, "PRED"))
                    text = "".join(ch.text for ch in chunks[j + 1 : neg_index])
                    out.append(Chunk((start, neg_index), text, "RAW"))
                elif pred_length > max_phrase_length and len(raw_indexs)>0:
                    raw_index = raw_indexs[0]
                    text = "".join(ch.text for ch in chunks[raw_index+1 : i + 1])        
                    out.append(Chunk((raw_index, end), text, "PRED"))
                    text = "".join(ch.text for ch in chunks[j + 1 : raw_index + 1])
                    out.append(Chunk((start, raw_index), text, "RAW"))
                else:
                    out.append(Chunk((start, end), text, "PRED"))
                    
                i = j
                continue            
        out.append(chunks[i])
        i -= 1

    return out[::-1]