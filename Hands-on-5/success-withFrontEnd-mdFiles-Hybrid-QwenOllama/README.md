# การตั้งค่าสภาพแวดล้อมและติดตั้งไลบรารีที่จำเป็น

## 1.1 Ollama
Ollama เป็นเครื่องมือที่ช่วยให้สามารถรันโมเดล LLM บนเครื่องคอมพิวเตอร์ส่วนตัวได้ โดยสามารถติดตั้งได้บนระบบปฏิบัติการหลักทั้ง macOS, Windows และ Linux

### การติดตั้ง Ollama บน Windows

ปัจจุบัน Ollama มีตัวติดตั้งสำหรับ Windows โดยตรงแล้ว คุณสามารถติดตั้งได้ดังนี้:

1. ไปที่เว็บไซต์ [https://ollama.com/download](https://ollama.com/download)
2. คลิกดาวน์โหลดเวอร์ชันสำหรับ Windows
3. เปิดไฟล์ติดตั้งที่ดาวน์โหลดมาและทำตามขั้นตอนการติดตั้ง
4. หลังจากติดตั้งเสร็จ โปรแกรม Ollama จะทำงานในพื้นหลังและคุณสามารถเข้าถึงได้ผ่าน Command Prompt หรือ PowerShell
5. ตรวจสอบการติดตั้งโดยเปิด Command Prompt และพิมพ์:
   ```
   ollama --version
   ```

### การติดตั้ง Ollama บน macOS และ Linux

สำหรับ macOS และ Linux คุณสามารถติดตั้งด้วยคำสั่ง:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

## 1.2 Docker Desktop
ติดตั้ง Docker Desktop: ดาวน์โหลดและติดตั้ง Docker Desktop จากเว็บไซต์อย่างเป็นทางการ (https://www.docker.com/products/docker-desktop/) ซึ่งจะใช้เพื่อรัน OpenSearch

สร้างเครือข่าย Docker แบบกำหนดเองชื่อ "opensearch-net" เพื่อสร้างสภาพแวดล้อมเครือข่ายแยกภายใน Docker ช่วยให้คอนเทนเนอร์สามารถสื่อสารกันได้อย่างปลอดภัย

```bash
docker network create opensearch-net
```

## 1.3 OpenSearch
รัน OpenSearch โดยใช้ Docker: เมื่อติดตั้งและรัน Docker Desktop แล้ว คุณสามารถเริ่ม OpenSearch ด้วยคำสั่งต่อไปนี้:

```bash
docker run -e OPENSEARCH_JAVA_OPTS="-Xms512m -Xmx512m" -e discovery.type="single-node" \
  -e DISABLE_SECURITY_PLUGIN="true" -e bootstrap.memory_lock="true" \
  -e cluster.name="opensearch-cluster" -e node.name="os01" \
  -e plugins.neural_search.hybrid_search_disabled="true" \
  -e DISABLE_INSTALL_DEMO_CONFIG="true" \
  --ulimit nofile="65536:65536" --ulimit memlock="-1:-1" \
  --net opensearch-net --restart=no \
  -v opensearch-data:/usr/share/opensearch/data \
  -p 9200:9200 \
  --name=opensearch-single-node \
  opensearchproject/opensearch:latest
```

คำสั่งนี้จะรัน OpenSearch ในคอนเทนเนอร์ Docker และทำให้สามารถเข้าถึงได้ที่พอร์ต 9200

## 1.4 Python Libraries
ตั้งค่าสภาพแวดล้อม Python: ตอนนี้ เราจะตั้งค่าสภาพแวดล้อม Python หากคุณใช้ Jupyter notebook คุณสามารถรันคำสั่งเหล่านี้โดยตรงในเซลล์:

```python
%pip install llama-index
%pip install llama-index-readers-elasticsearch
%pip install llama-index-vector-stores-opensearch
%pip install llama-index-embeddings-ollama
%pip install ollama
%pip install nest-asyncio
%pip install llama-index-embeddings-huggingface
```

นำเข้าโมดูลที่จำเป็นและตั้งค่าการกำหนดค่า:

```python
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext
from llama_index.core.node_parser import TokenTextSplitter
from llama_index.vector_stores.opensearch import OpensearchVectorStore, OpensearchVectorClient
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import torch
import nest_asyncio
from os import getenv

# ใช้ nest_asyncio เพื่อหลีกเลี่ยงข้อผิดพลาดในเวลารันใน Jupyter notebooks
nest_asyncio.apply()

# ตรวจสอบว่า CUDA พร้อมใช้งานสำหรับการเร่งความเร็ว GPU หรือไม่
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")
```

ในการตั้งค่าเหล่านี้ เราได้:

- ติดตั้ง Ollama สำหรับการรัน LLMs ในเครื่อง
- ตั้งค่า OpenSearch โดยใช้ Docker
- ติดตั้งไลบรารี Python ที่จำเป็น
- นำเข้าโมดูลที่ต้องการ
- ตั้งค่า CUDA สำหรับการเร่งความเร็ว GPU หากมี

ตอนนี้สภาพแวดล้อมของเราพร้อมใช้งานอย่างเต็มที่ด้วย Ollama และ OpenSearch ที่กำลังทำงาน เราพร้อมที่จะเริ่มประมวลผลเอกสาร PDF และสร้างระบบตอบคำถามของเรา ในส่วนต่อไป เราจะกล่าวถึงวิธีการโหลดและประมวลผลเอกสาร PDF โดยใช้ Llama Index

# 2. กำหนดค่าไปป์ไลน์การค้นหาแบบไฮบริด
ในขั้นตอนนี้ เราจะกำหนดค่าไปป์ไลน์การค้นหาแบบไฮบริดใน OpenSearch ไปป์ไลน์นี้รวมการค้นหาแบบดั้งเดิมที่ใช้คีย์เวิร์ดกับการค้นหาเวกเตอร์แบบความหมาย ช่วยให้ได้ผลลัพธ์ที่แม่นยำและเกี่ยวข้องกับบริบทมากขึ้น

```bash
curl -XPUT "http://localhost:9200/_search/pipeline/hybrid-search-pipeline" -H 'Content-Type: application/json' -d' \
{ \
  "description": "Pipeline for hybrid search", \
  "phase_results_processors": [ \
    { \
      "normalization-processor": { \
        "normalization": { \
          "technique": "min_max" \
        }, \
        "combination": { \
          "technique": "harmonic_mean", \
          "parameters": { \
            "weights": [ \
              0.3, \
              0.7 \
            ] \
          } \
        } \
      } \
    } \
  ] \
}'
```

มาแยกการกำหนดค่านี้:

### 2.1 API Endpoint
เรากำลังใช้คำขอ PUT ไปยัง OpenSearch API endpoint `/_search/pipeline/hybrid-search-pipeline` เพื่อสร้างหรืออัปเดตไปป์ไลน์การค้นหาชื่อ "hybrid-search-pipeline"

### 2.2 การกำหนดค่าไปป์ไลน์
- `description`: ให้คำอธิบายสั้นๆ เกี่ยวกับวัตถุประสงค์ของไปป์ไลน์
- `phase_results_processors`: กำหนดโปรเซสเซอร์ที่จะนำไปใช้กับผลลัพธ์การค้นหา

### 2.3 โปรเซสเซอร์การทำให้เป็นมาตรฐาน
- `normalization`: ใช้เทคนิค "min_max" เพื่อทำให้คะแนนจากวิธีการค้นหาที่แตกต่างกัน (คีย์เวิร์ดและความหมาย) เป็นมาตรฐานเดียวกัน
- `combination`: ระบุวิธีการรวมคะแนนที่เป็นมาตรฐานแล้ว:
  - `technique`: ใช้ "harmonic_mean" เพื่อรวมคะแนน
  - `weights`: [0.3, 0.7] กำหนดน้ำหนักที่แตกต่างกันให้กับวิธีการค้นหาสองวิธี ในกรณีนี้ การค้นหาเชิงความหมาย (การค้นหาเวกเตอร์) ได้รับน้ำหนักมากกว่า (0.7) เมื่อเทียบกับการค้นหาคีย์เวิร์ด (0.3)

วิธีการแบบไฮบริดนี้ช่วยให้เราใช้ประโยชน์จากทั้งความเร็วของการค้นหาคีย์เวิร์ดและความเข้าใจในบริบทของการค้นหาเชิงความหมาย โดยการกำหนดน้ำหนักสูงกว่าให้กับการค้นหาเชิงความหมาย เราให้ความสำคัญกับผลลัพธ์ที่เกี่ยวข้องกับคำถามในเชิงแนวคิดมากกว่า ในขณะที่ยังพิจารณาการจับคู่คีย์เวิร์ดที่ตรงกันอย่างแม่นยำ

การใช้ curl ในขั้นตอนนี้สันนิษฐานว่าคุณกำลังรันในสภาพแวดล้อมคล้าย Unix หรือใช้ WSL บน Windows หากคุณอยู่ในสภาพแวดล้อมที่แตกต่างกัน คุณอาจต้องปรับคำสั่งนี้หรือใช้วิธีอื่นเพื่อส่งคำขอ HTTP ไปยัง OpenSearch

# 3. โหลดและประมวลผลเอกสาร PDF
ในขั้นตอนนี้ เราจะโหลดเอกสาร PDF และแปลงเป็นรูปแบบที่เหมาะสำหรับการประมวลผลเพิ่มเติม โดยใช้ Llama Index เพื่อช่วยจัดการข้อมูล

### 3.1 โหลดเอกสาร PDF:
```python
from llama_index.core import SimpleDirectoryReader
reader = SimpleDirectoryReader(input_dir="pdf_corpus", recursive=True)
documents = reader.load_data()
```

คำอธิบาย: เราใช้ SimpleDirectoryReader เพื่อโหลดไฟล์ PDF จากไดเรกทอรีที่ระบุ ฟังก์ชันนี้เป็นส่วนหนึ่งของ Llama Index และออกแบบมาเพื่อจัดการรูปแบบเอกสารต่างๆ รวมถึง PDF มันสกัดเนื้อหาข้อความจาก PDF โดยอัตโนมัติ ทำให้ง่ายต่อการประมวลผลข้อมูลในขั้นตอนต่อไป

### 3.2 แบ่งเอกสารเป็นชิ้นส่วน:
```python
from llama_index.core.node_parser import TokenTextSplitter
splitter = TokenTextSplitter(
    chunk_size=512,
    chunk_overlap=128,
    separator=" ",
)
token_nodes = splitter.get_nodes_from_documents(
    documents, show_progress=True
)
```

คำอธิบาย: เราใช้ TokenTextSplitter เพื่อแบ่งเอกสารเป็นส่วนย่อยที่จัดการได้ง่ายที่เรียกว่า "token_nodes"

- `chunk_size=512`: กำหนดจำนวนโทเค็นสูงสุดในแต่ละชิ้นส่วน (แต่ละโหนด) เราเลือก 512 เนื่องจากเป็นขนาดทั่วไปที่สมดุลระหว่างการมีบริบทเพียงพอและไม่ทำให้โมเดลถูกครอบงำ
- `chunk_overlap=128`: อนุญาตให้มีการซ้อนทับบางส่วนระหว่างชิ้นส่วน ซึ่งช่วยรักษาบริบทข้ามขอบเขตของชิ้นส่วน การซ้อนทับของโทเค็น 128 ตัวช่วยให้แน่ใจว่าเราไม่สูญเสียข้อมูลสำคัญที่อาจแบ่งระหว่างสองชิ้นส่วน

# 4. สร้าง embeddings โดยใช้โมเดล BAAI/bge-m3
ในขั้นตอนนี้ เราจะใช้โมเดล BAAI/bge-m3 เพื่อสร้าง embeddings สำหรับชิ้นส่วนข้อความของเรา embeddings เหล่านี้มีความสำคัญสำหรับการค้นหาเชิงความหมายและการทำความเข้าใจเนื้อหาของเอกสารของเรา

```python
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
embedding_model_name = 'BAAI/bge-m3'
embedding_model = HuggingFaceEmbedding(model_name=embedding_model_name, max_length=512, device=device)
embeddings = embedding_model.get_text_embedding("box")
dim = len(embeddings)
print("embedding dimension of example text ===>", dim)
```

ในโค้ดนี้:

- เราตั้งค่าโมเดล BAAI/bge-m3 โดยใช้คลาส HuggingFaceEmbedding กำหนดความยาวสูงสุดเป็น 512 โทเค็นและใช้อุปกรณ์ (CPU หรือ GPU) ที่เรากำหนดไว้ก่อนหน้านี้
- เราใช้เมธอด get_text_embedding_batch เพื่อสร้าง embeddings อย่างมีประสิทธิภาพสำหรับโหนดข้อความทั้งหมดของเราในครั้งเดียว
- เราพิมพ์จำนวน embeddings ที่สร้างขึ้น
- เราสร้าง embedding ตัวอย่างสำหรับคำว่า "box" เพื่อกำหนดมิติของ embeddings ของเราและพิมพ์ข้อมูลนี้

โมเดล BAAI/bge-m3 ได้รับการออกแบบมาโดยเฉพาะสำหรับการสร้าง embeddings คุณภาพสูงสำหรับงานค้นหาเชิงความหมาย โดยการใช้โมเดลนี้ เราทำให้แน่ใจว่า embeddings ของเราจับความหมายเชิงความหมายของชิ้นส่วนข้อความของเราอย่างมีประสิทธิภาพ

embeddings เหล่านี้จะถูกใช้ในขั้นตอนต่อไปสำหรับการทำดัชนีและค้นหาเนื้อหาเอกสารของเรา ช่วยให้เราสามารถค้นหาข้อมูลที่เกี่ยวข้องมากที่สุดเมื่อตอบคำถามเกี่ยวกับ PDF ของเรา

# 5. ตั้งค่าและเริ่มต้น OpenSearch Vector Client
ในขั้นตอนนี้ เราจะตั้งค่าและเริ่มต้น OpenSearch Vector Client เตรียมระบบของเราให้ใช้ OpenSearch เป็นฐานข้อมูลเวกเตอร์สำหรับการค้นหาความคล้ายคลึงอย่างมีประสิทธิภาพในอนาคต

### 5.1 ตั้งค่ารายละเอียดการเชื่อมต่อ OpenSearch
```python
from os import getenv
from llama_index.vector_stores.opensearch import (
    OpensearchVectorStore,
    OpensearchVectorClient,
)

# http endpoint สำหรับคลัสเตอร์ของคุณ (จำเป็นต้องใช้ opensearch สำหรับการใช้ดัชนีเวกเตอร์)
endpoint = getenv("OPENSEARCH_ENDPOINT", "http://localhost:9200")
# ดัชนีเพื่อแสดงการใช้งาน VectorStore
idx = getenv("OPENSEARCH_INDEX", "test_pdf_index")
```

เราใช้ getenv เพื่อดึงข้อมูล OpenSearch endpoint และชื่อดัชนีจากตัวแปรสภาพแวดล้อม โดยมีค่าเริ่มต้นที่ให้ไว้ วิธีนี้ช่วยให้การเปลี่ยนแปลงการกำหนดค่าได้ง่ายข้ามสภาพแวดล้อมที่แตกต่างกันโดยไม่ต้องแก้ไขโค้ด

### 5.2 กำหนดค่า OpenSearchVectorClient
```python
# OpensearchVectorClient จัดเก็บข้อความในฟิลด์นี้ตามค่าเริ่มต้น
text_field = "content_text"
# OpensearchVectorClient จัดเก็บ embeddings ในฟิลด์นี้ตามค่าเริ่มต้น
embedding_field = "embedding"
# OpensearchVectorClient รวมตรรกะสำหรับดัชนี opensearch เดียวที่เปิดใช้งานการค้นหาเวกเตอร์ด้วยไปป์ไลน์การค้นหาแบบไฮบริด
client = OpensearchVectorClient(
    endpoint=endpoint,
    index=idx,
    dim=dim,
    embedding_field=embedding_field,
    text_field=text_field,
    search_pipeline="hybrid-search-pipeline",
)
```

เราสร้าง OpensearchVectorClient ด้วยการกำหนดค่าเฉพาะ:

- `endpoint` และ `index`: ระบุว่าจะเชื่อมต่อกับ OpenSearch ที่ไหนและจะใช้ดัชนีใด
- `dim`: กำหนดมิติของเวกเตอร์ embedding ซึ่งต้องตรงกับมิติของ embeddings ที่เราสร้างขึ้น
- `embedding_field` และ `text_field`: กำหนดชื่อฟิลด์สำหรับการจัดเก็บ embeddings และเนื้อหาข้อความตามลำดับ
- `search_pipeline`: ระบุการใช้ "hybrid-search-pipeline" ที่รวมการค้นหาแบบคีย์เวิร์ดและความหมายเพื่อผลลัพธ์ที่ดีขึ้น

### 5.3 เริ่มต้น OpensearchVectorStore
```python
# เริ่มต้น vector store
vector_store = OpensearchVectorStore(client)
```

เราสร้างอินสแตนซ์ของ OpensearchVectorStore โดยใช้ไคลเอนต์ที่กำหนดค่าไว้ ซึ่งให้อินเทอร์เฟซสำหรับการจัดการ vector store ภายในเฟรมเวิร์ก Llama Index ช่วยให้การรวมกับฟังก์ชัน Llama Index อื่นๆ ได้ง่าย

วิธีการที่มีโครงสร้างนี้เตรียมระบบของเราสำหรับการจัดเก็บและการเรียกค้น embeddings ในอนาคตโดยใช้ความสามารถในการค้นหาเวกเตอร์ของ OpenSearch ไปป์ไลน์การค้นหาแบบไฮบริดช่วยให้การค้นหาที่ซับซ้อนมากขึ้น ซึ่งอาจปรับปรุงความแม่นยำและความเกี่ยวข้องของกระบวนการเรียกค้นเอกสารของเรา การจัดเก็บ embeddings จะเกิดขึ้นในขั้นตอนต่อไป

ในสภาพแวดล้อมการผลิต แนะนำให้ใช้การจัดการข้อผิดพลาดและการตรวจสอบการเชื่อมต่อเพื่อให้แน่ใจว่าการทำงานมีความแข็งแกร่ง นอกจากนี้ คุณอาจต้องการทดสอบการเชื่อมต่อและดำเนินการง่ายๆ เพื่อยืนยันว่าทุกอย่างตั้งค่าถูกต้องก่อนที่จะดำเนินการกับขั้นตอนต่อไป

# 6. สร้าง VectorStoreIndex และจัดเก็บ Embeddings
ในขั้นตอนนี้ เราจะสร้าง VectorStoreIndex โดยใช้ Llama Index และจัดเก็บ embeddings เอกสารของเราใน OpenSearch อย่างชัดเจน กระบวนการนี้ช่วยให้การค้นหาเชิงความหมายและการเรียกค้นข้อมูลจากเอกสารที่ประมวลผลของเรามีประสิทธิภาพ

### 6.1 สร้าง StorageContext
```python
from llama_index.core import VectorStoreIndex, StorageContext

storage_context = StorageContext.from_defaults(vector_store=vector_store)
```

ที่นี่ เราสร้าง StorageContext โดยใช้ vector_store (OpenSearch) ที่เราเริ่มต้นในขั้นตอนก่อนหน้า StorageContext นี้ให้อินเทอร์เฟซมาตรฐานสำหรับการจัดการการจัดเก็บใน Llama Index และเชื่อมต่อดัชนีของเรากับ OpenSearch vector store

### 6.2 สร้าง VectorStoreIndex, สร้างและจัดเก็บ Embeddings
```python
index = VectorStoreIndex(
    token_nodes, storage_context=storage_context, embed_model=embedding_model
)
```

ในขั้นตอนสำคัญนี้ เราสร้าง VectorStoreIndex, สร้าง embeddings สำหรับเอกสารของเรา และจัดเก็บใน OpenSearch:

- `token_nodes`: โหนดเอกสารที่ประมวลผลแล้วที่สร้างไว้ก่อนหน้านี้
- `storage_context`: บริบทการจัดเก็บที่เราเพิ่งสร้าง เชื่อมโยงกับ OpenSearch vector store ของเรา
- `embedding_model`: โมเดล embedding ที่เรากำลังใช้ (BAAI/bge-m3 ในกรณีนี้)

การดำเนินการนี้ทำงานสำคัญหลายอย่าง:

- มันสร้าง embeddings สำหรับแต่ละโหนดเอกสารโดยใช้ embedding_model ที่ระบุ
- จากนั้นจะจัดเก็บ embeddings เหล่านี้ใน OpenSearch vector store ที่กำหนดไว้ใน storage_context ของเรา OpenSearch จัดการการจัดเก็บและการทำดัชนีของ vector embeddings เหล่านี้อย่างมีประสิทธิภาพ
- สุดท้าย Llama Index สร้างโครงสร้างที่ค้นหาได้ภายในของตัวเอง ซึ่ง: (a) สร้างดัชนีท้องถิ่นเพื่อจัดเก็บเมตาดาต้าเอกสารและการอ้างอิงไปยัง embeddings ใน OpenSearch (b) สร้างโครงสร้างข้อมูลที่มีประสิทธิภาพเพื่อเปิดใช้งานการค้นหาความคล้ายคลึงอย่างรวดเร็วและการเรียกค้นเอกสารที่เกี่ยวข้อง

หมายเหตุ: คุณสามารถตรวจสอบว่า embeddings ถูกจัดเก็บใน OpenSearch โดยการตรวจสอบดัชนี OpenSearch หลังจากการดำเนินการนี้ embeddings จะถูกเก็บไว้ในฟิลด์ที่ระบุเมื่อตั้งค่า OpenSearchVectorClient (โดยทั่วไปคือ "embedding")

VectorStoreIndex ทำหน้าที่เป็นสะพานระหว่างเอกสารที่ประมวลผลแล้ว embeddings ที่จัดเก็บใน OpenSearch และเฟรมเวิร์ก Llama Index มันช่วยให้เราสามารถทำการค้นหาความคล้ายคลึงเชิงความหมายอย่างรวดเร็วเมื่อสอบถามเอกสารของเราในขั้นตอนต่อไป โดยใช้ความสามารถในการค้นหาเวกเตอร์ของ OpenSearch

โดยการสร้างดัชนีนี้และจัดเก็บ embeddings ใน OpenSearch อย่างชัดเจน เรากำลังสร้างระบบที่สามารถค้นหาและเรียกค้นข้อมูลที่เกี่ยวข้องจากเอกสาร PDF ที่ประมวล