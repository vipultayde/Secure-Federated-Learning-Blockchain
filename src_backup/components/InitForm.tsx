import React, { useState } from 'react';
import { api } from '../api/client';

interface Props {
    onInit: () => void;
}

export const InitForm: React.FC<Props> = ({ onInit }) => {
    const [numClients, setNumClients] = useState(5);
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        try {
            await api.init({
                num_clients: numClients,
                local_epochs: 1,
                learning_rate: 0.01
            });
            onInit();
        } catch (error) {
            console.error(error);
            alert("Failed to initialize");
        }
        setLoading(false);
    };

    return (
        <form onSubmit={handleSubmit} className="bg-white p-4 rounded shadow mb-4">
            <h3 className="text-lg font-bold mb-4">Experiment Setup</h3>
            <div className="mb-4">
                <label className="block text-gray-700 text-sm font-bold mb-2">
                    Number of Clients
                </label>
                <input
                    type="number"
                    value={numClients}
                    onChange={(e) => setNumClients(parseInt(e.target.value))}
                    className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                    min="1"
                    max="20"
                />
            </div>
            <button
                type="submit"
                disabled={loading}
                className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline disabled:opacity-50"
            >
                {loading ? 'Initializing...' : 'Initialize Experiment'}
            </button>
        </form>
    );
};
