// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract FLRegistry {
    struct Contribution {
        uint256 clientId;
        uint256 samples;
        uint256 accuracy; // Scaled by 1e4 (e.g., 95.5% = 9550)
        uint256 loss;     // Scaled by 1e4
        bool malicious;
        bool accepted;
    }

    struct RoundBlock {
        uint256 roundId;
        string modelHash;
        uint256 globalAccuracy; // Scaled by 1e4
        uint256 timestamp;
        Contribution[] contributions;
    }

    RoundBlock[] public chain;

    event RoundAdded(uint256 indexed roundId, string modelHash, uint256 globalAccuracy);

    function addRound(
        string memory _modelHash,
        uint256 _globalAccuracy,
        Contribution[] memory _contributions
    ) public {
        uint256 roundId = chain.length;
        RoundBlock storage newBlock = chain.push();
        newBlock.roundId = roundId;
        newBlock.modelHash = _modelHash;
        newBlock.globalAccuracy = _globalAccuracy;
        newBlock.timestamp = block.timestamp;
        
        for (uint i = 0; i < _contributions.length; i++) {
            newBlock.contributions.push(_contributions[i]);
        }

        emit RoundAdded(roundId, _modelHash, _globalAccuracy);
    }

    function getChainLength() public view returns (uint256) {
        return chain.length;
    }

    function getRound(uint256 _index) public view returns (
        uint256 roundId,
        string memory modelHash,
        uint256 globalAccuracy,
        uint256 timestamp,
        Contribution[] memory contributions
    ) {
        RoundBlock storage b = chain[_index];
        return (b.roundId, b.modelHash, b.globalAccuracy, b.timestamp, b.contributions);
    }
}
