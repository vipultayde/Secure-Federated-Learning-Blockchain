export interface InitRequest {
    num_clients: number;
    local_epochs: number;
    learning_rate: number;
}

export interface Block {
    index: number;
    timestamp: number;
    previous_hash: string;
    model_hash: string;
    round_metrics: Record<string, number>;
    client_contributions: any[];
    hash: string;
}

export interface ChainResponse {
    blocks: Block[];
}

export interface RoundResponse {
    round_id: number;
    global_accuracy: number;
    block_hash: string;
}
