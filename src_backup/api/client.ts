import type { InitRequest, ChainResponse, RoundResponse } from '../types';

const API_URL = 'http://localhost:8000/api';

export const api = {
    init: async (data: InitRequest) => {
        const response = await fetch(`${API_URL}/init`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });
        return response.json();
    },
    runRound: async (malicious_indices: number[] = [], defense_enabled: boolean = false): Promise<RoundResponse> => {
        const response = await fetch(`${API_URL}/round`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ malicious_indices, defense_enabled }),
        });
        return response.json();
    },
    getChain: async (): Promise<ChainResponse> => {
        const response = await fetch(`${API_URL}/chain`);
        return response.json();
    },
    getMetrics: async () => {
        const response = await fetch(`${API_URL}/metrics`);
        return response.json();
    }
};
