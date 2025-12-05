import grpc
import time
import csv
import matplotlib.pyplot as plt 
import dist_calc_pb2
import dist_calc_pb2_grpc

def run_benchmark():
    channel = grpc.insecure_channel('192.168.1.14:50051')
    stub = dist_calc_pb2_grpc.DistributedCalculatorStub(channel)

    print("\n" + "#"*50)
    print(" INICIANDO BENCHMARK DE PERFORMANCE gRPC")
    print("#"*50)
    
    test_loads = [1, 10, 100, 1000, 5000, 10000, 50000, 100000]
    payload_fixed = 100  
    results = []

    print(f"{'OPS':<10} | {'SERVER(ms)':<12} | {'TOTAL(ms)':<12} | {'REDE(ms)':<12}")
    print("-" * 52)

    try:
        for ops in test_loads:
            
            start_time = time.time()
            
            response = stub.Workload(dist_calc_pb2.WorkloadRequest(
                operations=ops, 
                payload_size=payload_fixed
            ))
            
            end_time = time.time()
            
            total_time_ms = (end_time - start_time) * 1000
            server_time_ms = response.time_ms 
            network_latency = total_time_ms - server_time_ms 
            
            print(f"{ops:<10} | {server_time_ms:<12.4f} | {total_time_ms:<12.4f} | {network_latency:<12.4f}")
            
            results.append({
                "operations": ops,
                "server_time": server_time_ms,
                "total_time": total_time_ms,
                "latency_est": network_latency
            })

    except grpc.RpcError as e:
        print(f"\n[ERRO] Falha gRPC: {e}")
        return

    csv_filename = 'resultados_benchmark.csv'
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Operacoes", "Tempo_Servidor_ms", "Tempo_Total_ms", "Latencia_Rede_ms"])
        for r in results:
            writer.writerow([r["operations"], r["server_time"], r["total_time"], r["latency_est"]])
    
    print("-" * 52)
    print(f"Dados salvos em '{csv_filename}'")
    print("Gerando gráfico...")

    ops_x = [r["operations"] for r in results]
    server_y = [r["server_time"] for r in results]
    total_y = [r["total_time"] for r in results]

    plt.figure(figsize=(10, 6))
    
    plt.xscale('log') 
    
    plt.plot(ops_x, total_y, marker='o', label='Tempo Total (Cliente)', linestyle='-')
    plt.plot(ops_x, server_y, marker='x', label='Tempo Processamento (Servidor)', linestyle='--')
    
    plt.xlabel('Número de Operações (Log)')
    plt.ylabel('Tempo (ms)')
    plt.title('Performance: Tempo Total vs Tempo de Processamento')
    plt.legend()
    plt.grid(True, which="both", ls="-", alpha=0.5)
    
    print("Gráfico gerado. Exibindo na tela...")
    plt.show()

if __name__ == '__main__':
    run_benchmark()