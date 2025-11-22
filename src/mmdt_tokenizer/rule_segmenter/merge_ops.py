from typing import List
from .types import Chunk
from .lexicon import FUN_TAG


def merge_num_classifier(chunks: List[Chunk]) -> List[Chunk]:
    out: List[Chunk] = []
    i = 0
    n = len(chunks)
    NUMBER_TAGS = ("NUM", "WORDNUM")
    CL_TAGS = ("CL", "CLEP")
    COMMON_KEYS_PRE = {'ဦး', "ရက်", "ပင်", "တို့"}
    PERCENT_WORD = "ရာခိုင်နှုန်း"
    
    while i< n: 
        cur = chunks[i]

        if cur.text == PERCENT_WORD:
            out.append(Chunk(cur.span, cur.text, "INUMCL"))
            i += 1
            continue

        if cur.tag in NUMBER_TAGS:
            num_start = cur.span[0]
            j = i

            # Merge NUM and punctuation inside the number
            while j < n and (chunks[j].tag in NUMBER_TAGS or chunks[j].tag == "PUNCT"):
                j += 1

            num_text = "".join(c.text for c in chunks[i:j]).strip().replace(" ", "")
            num_end = chunks[j - 1].span[1]
            out.append(Chunk((num_start, num_end), num_text, "NUM"))

            # add classifier term
            k = j
            if k < n and (chunks[k].tag in CL_TAGS or chunks[k].text in COMMON_KEYS_PRE):
                cl_start = chunks[k].span[0]

                while k < n and (chunks[k].tag in CL_TAGS or chunks[k].text in COMMON_KEYS_PRE):
                    k += 1

                cl_text = "".join(c.text for c in chunks[j:k]).strip().replace(" ", "")
                cl_end = chunks[k - 1].span[1]
                out.append(Chunk((cl_start, cl_end), cl_text, "NUMCL"))

            i = k
            continue

        out.append(cur)
        i +=1
    return out

def merge_predicate(chunks: List["Chunk"]) -> List["Chunk"]:
    n = len(chunks)
    i = n - 1
    out = []
    
    neg_sent_sfp = ("ပါ", "ဘူး", "နဲ့", "နှင့်")
    que_sent_sfp = ("နည်း", 'လား', 'လဲ', 'တုံး')
    neg_prefix = "မ"
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
            sfp_vep_index = None
            while j >= 0 and chunks[j].tag in ("SFP", "VEP", "RAW", "QW"): 
                if chunks[j].tag == "RAW": raw_indexs.append(j)
                if chunks[j].text == neg_prefix and neg_index is None: neg_index = j
                if chunks[j].tag == "QW" and que_index is None: que_index = j
                if chunks[j].tag in ("SFP", "VEP"): sfp_vep_index = j 
                j -= 1
            pred_length = i - j
            if pred_length > 1 :
                start = chunks[j + 1].span[0]
                end = chunks[i].span[1]
                text = "".join(ch.text for ch in chunks[j + 1 : i + 1])
         
                if neg_index is not None and chunks[i].text in neg_sent_sfp: 
                    text = "".join(ch.text for ch in chunks[neg_index : i + 1]) 
                    pred_start = chunks[neg_index].span[0]       
                    out.append(Chunk((pred_start, end), text, "PRED"))
                    text = "".join(ch.text for ch in chunks[j + 1 : neg_index])
                    raw_end = chunks[neg_index-1].span[1]
                    out.append(Chunk((start,raw_end), text, "RAW"))
                
                elif que_index is not None and chunks[i].text in que_sent_sfp: 
                    text = "".join(ch.text for ch in chunks[que_index : i + 1])  
                    pred_start = chunks[que_index].span[0]            
                    out.append(Chunk((pred_start, end), text, "PRED"))
                    text = "".join(ch.text for ch in chunks[j + 1 : que_index])
                    que_end = chunks[que_index-1].span[1]
                    out.append(Chunk((start, que_end), text, "RAW"))

                else:
                    # positive pred
                    if sfp_vep_index is not None:
                        k = sfp_vep_index
                        pred_part = chunks[k : i + 1]
                        
                        if(len(pred_part)>1):
                            pred_text = "".join(ch.text for ch in pred_part)
                            pred_start = pred_part[0].span[0]
                            pred_end = pred_part[-1].span[1]
                            out.append(Chunk((pred_start, pred_end), pred_text, "PRED"))
                            
                        else:
                            pred_start = chunks[k].span[0]
                            pred_end = chunks[i].span[1]
                            pred_text = chunks[k].text
                            k_index = k +1
                            #check if it is last in the sentence
                            while k_index<n and chunks[k_index].tag == "PUNCT": k_index+=1
                            if (k_index == n):
                                out.append(Chunk((pred_start, pred_end), pred_text, "PRED"))
                            else:
                                out.append(Chunk((pred_start, pred_end), pred_text, "SFP"))

                        #lead unseen part
                        for t in range(k - 1, j, -1):
                                out.append(chunks[t])
                        

     
                i = j
                continue     

        out.append(chunks[i])
        i -= 1
    return out[::-1]