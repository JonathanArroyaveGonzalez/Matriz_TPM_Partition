import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import logging
import time
from scipy.stats import wasserstein_distance
from typing import Dict, Set

class PartitionAnalyzer:
    def __init__(self, tpm: np.ndarray, present_nodes: str, future_nodes: str):
        """Inicializa el analizador de particiones"""
        self.tpm = tpm
        self.present_nodes = list(present_nodes)
        self.future_nodes = list(future_nodes)
        self.best_partition = None
        self.min_loss = float('inf')
        logging.info(f"Analizador inicializado: presente={present_nodes}, futuro={future_nodes}")

    def analyze_partitions(self) -> Dict:
        """Implementa la estrategia #2 para análisis de particiones"""
        start_time = time.time()
        edges = [(p, f) for p in self.present_nodes for f in self.future_nodes]
        
        # Implementar algoritmo de la estrategia #2
        W = [set()]  # W₀ = ∅
        W.append({edges[0]})  # W₁ = {a₁}
        
        for i in range(2, len(edges) + 1):
            remaining_edges = set(edges) - W[i-1]
            min_diff = float('inf')
            best_edge = None
            
            for edge in remaining_edges:
                current_loss = self._calculate_loss(W[i-1] | {edge})
                single_loss = self._calculate_loss({edge})
                diff = current_loss - single_loss
                
                if diff < min_diff:
                    min_diff = diff
                    best_edge = edge
            
            if best_edge:
                W.append(W[i-1] | {best_edge})
                if self._is_valid_partition(W[i]):
                    loss = self._calculate_loss(W[i])
                    if loss < self.min_loss:
                        self.min_loss = loss
                        self.best_partition = W[i]
        
        execution_time = time.time() - start_time
        
        return {
            'best_partition': self.best_partition,
            'min_loss': self.min_loss,
            'execution_time': execution_time
        }

    def _calculate_loss(self, edge_set: Set) -> float:
        """Calcula la pérdida usando EMD"""
        # Implementación del cálculo de EMD
        return wasserstein_distance(self.tpm.flatten(), np.zeros_like(self.tpm.flatten()))

    def _is_valid_partition(self, edge_set: Set) -> bool:
        """Verifica si el conjunto de aristas forma una partición válida"""
        G = nx.Graph()
        for edge in edge_set:
            G.add_edge(edge[0], edge[1])
        try:
            colors = nx.bipartite.color(G)
            return True
        except:
            return False

    def visualize_partition(self, filename: str):
        """Visualiza la partición"""
        if not self.best_partition:
            logging.warning("No hay partición para visualizar")
            return
            
        G = nx.DiGraph()
        
        pos = {}
        for i, node in enumerate(self.present_nodes):
            pos[node] = (0, i)
        for i, node in enumerate(self.future_nodes):
            pos[node] = (1, i)
            
        for edge in self.best_partition:
            G.add_edge(edge[0], edge[1])
            
        plt.figure(figsize=(10, 8))
        nx.draw(G, pos, with_labels=True, node_color='lightblue',
               node_size=500, arrowsize=20)
        plt.title("Partición del Sistema")
        plt.savefig(filename)
        plt.close()
        
        logging.info(f"Visualización guardada como {filename}")