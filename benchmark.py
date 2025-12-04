import grpc
import time
import csv
import matplotlib.pyplot as plt 
import dist_calc_pb2
import dist_calc_pb2_grpc

def run_benchmark():
    channel = grpc.insecure_channel('192.168.1.14:50051')
    stub = dist_calc_pb2_grpc.DistributedCalculatorStub(channel)

    print("Iniciando Benchmark do Middleware gRPC...")
    
    test_loads = [1, 10, 100, 1000, 5000, 10000, 50000, 100000]
    payload_fixed = 100  
    results = []

    try:
        for ops in test_loads:
            print(f"Testando carga: {ops} operações...")

            start_time = time.time()
            
            response = stub.Workload(dist_calc_pb2.WorkloadRequest(
                operations=ops, 
                payload_size=payload_fixed
            ))
            
            end_time = time.time()
            
            total_time_ms = (end_time - start_time) * 1000
            server_time_ms = response.time_ms 
            network_latency = total_time_ms - server_time_ms 
            
            results.append({
                "operations": ops,
                "server_time": server_time_ms,
                "total_time": total_time_ms,
                "latency_est": network_latency
            })

    except grpc.RpcError as e:
        print(f"Erro gRPC: {e}")
        return

    csv_filename = 'resultados_benchmark.csv'
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Operacoes", "Tempo_Servidor_ms", "Tempo_Total_ms", "Latencia_Rede_ms"])
        for r in results:
            writer.writerow([r["operations"], r["server_time"], r["total_time"], r["latency_est"]])
    
    print(f"\nDados salvos em {csv_filename}")

    ops_x = [r["operations"] for r in results]
    server_y = [r["server_time"] for r in results]
    total_y = [r["total_time"] for r in results]

    plt.figure(figsize=(10, 6))
    plt.plot(ops_x, total_y, marker='o', label='Tempo Total (Cliente)', linestyle='-')
    plt.plot(ops_x, server_y, marker='x', label='Tempo Processamento (Servidor)', linestyle='--')
    
    plt.title('Performance do Middleware gRPC: Carga vs Tempo')
    plt.xlabel('Número de Operações (Carga)')
    plt.ylabel('Tempo (ms)')
    plt.legend()
    plt.grid(True)
    
    plt.savefig('grafico_benchmark.png')
    print("Gráfico salvo como grafico_benchmark.png")
    plt.show()

if __name__ == '__main__':
    run_benchmark()