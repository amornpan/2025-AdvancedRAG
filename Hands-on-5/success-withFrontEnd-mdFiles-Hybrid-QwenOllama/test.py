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