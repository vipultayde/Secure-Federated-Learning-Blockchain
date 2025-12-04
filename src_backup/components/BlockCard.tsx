import React from 'react';
import type { Block } from '../types';

interface Props {
    block: Block;
}

export const BlockCard: React.FC<Props> = ({ block }) => {
    return (
        <div className="border p-4 m-2 rounded shadow">
            <h3 className="font-bold">Block #{block.index}</h3>
            <p className="text-sm text-gray-600">{new Date(block.timestamp * 1000).toLocaleString()}</p>
            <div className="mt-2">
                <p>Model Hash: {block.model_hash.substring(0, 10)}...</p>
                <p>Prev Hash: {block.previous_hash.substring(0, 10)}...</p>
            </div>
        </div>
    );
};
