import React, { useEffect, useState } from 'react';
import { api } from '../api/client';
import type { Block } from '../types';
import { BlockCard } from '../components/BlockCard';
import { InitForm } from '../components/InitForm';
import { TrainingChart } from '../components/TrainingChart';

export const Dashboard: React.FC = () => {
    const [chain, setChain] = useState<Block[]>([]);
    const [metrics, setMetrics] = useState<any[]>([]);
    const [loading, setLoading] = useState(false);

    const fetchData = async () => {
        try {
            const chainData = await api.getChain();
            setChain(chainData.blocks);
            const metricsData = await api.getMetrics();
            setMetrics(metricsData.metrics);
        } catch (e) {
            console.error("Failed to fetch data", e);
        }
    };

    useEffect(() => {
        fetchData();
    }, []);

    const [maliciousEnabled, setMaliciousEnabled] = useState(false);
    const [defenseEnabled, setDefenseEnabled] = useState(false);

    const handleRunRound = async () => {
        setLoading(true);
        try {
            const maliciousIndices = maliciousEnabled ? [0] : [];
            await api.runRound(maliciousIndices, defenseEnabled);
            await fetchData();
        } catch (e) {
            console.error(e);
            alert("Failed to run round");
        }
        setLoading(false);
    };

    return (
        <div className="p-8 max-w-7xl mx-auto">
            <h1 className="text-3xl font-bold mb-8 text-gray-800">Secure Federated Learning Blockchain</h1>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
                <div className="lg:col-span-1">
                    <InitForm onInit={fetchData} />

                    <div className="bg-white p-4 rounded shadow mt-4">
                        <h3 className="text-lg font-bold mb-4">Control Panel</h3>

                        <div className="mb-4 space-y-2">
                            <label className="flex items-center space-x-2">
                                <input
                                    type="checkbox"
                                    checked={maliciousEnabled}
                                    onChange={(e) => setMaliciousEnabled(e.target.checked)}
                                    className="form-checkbox h-5 w-5 text-red-600"
                                />
                                <span className="text-gray-700">Simulate Malicious Client #0</span>
                            </label>
                            <label className="flex items-center space-x-2">
                                <input
                                    type="checkbox"
                                    checked={defenseEnabled}
                                    onChange={(e) => setDefenseEnabled(e.target.checked)}
                                    className="form-checkbox h-5 w-5 text-green-600"
                                />
                                <span className="text-gray-700">Enable Server Defense</span>
                            </label>
                        </div>

                        <button
                            onClick={handleRunRound}
                            disabled={loading || chain.length === 0}
                            className="w-full bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            {loading ? 'Running Round...' : 'Run Training Round'}
                        </button>
                        <div className="mt-4 text-sm text-gray-600">
                            Current Round: {chain.length > 0 ? chain.length - 1 : 0}
                        </div>
                    </div>
                </div>

                <div className="lg:col-span-2">
                    <TrainingChart data={metrics} />
                </div>
            </div>

            <h2 className="text-2xl font-bold mb-4 text-gray-800">Blockchain Ledger</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {chain.slice().reverse().map((block) => (
                    <BlockCard key={block.hash} block={block} />
                ))}
            </div>
        </div>
    );
};
