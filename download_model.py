from huggingface_hub import snapshot_download
snapshot_download(
    repo_id='BAAI/bge-m3',
    local_dir='/media/lyg/edata/models/bge-m3',
    ignore_patterns=['*.pt', 'flax*', 'tf_*'],
)