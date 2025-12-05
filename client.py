import grpc
import time
import dist_calc_pb2
import dist_calc_pb2_grpc

def run():
    print("Tentando conectar ao servidor...")
    channel = grpc.insecure_channel('192.168.1.14:50051')
    stub = dist_calc_pb2_grpc.DistributedCalculatorStub(channel)
    print("Conectado!\n")
    
    print("="*40)
    print(" TESTE 1: SOMA SIMPLES")
    print("="*40)
    val_a = 10.5
    val_b = 20.3
    
    print(f"[CLIENTE] Enviando solicitação: {val_a} + {val_b}")
    response_sum = stub.Sum(dist_calc_pb2.SumRequest(a=val_a, b=val_b))
    print(f"[CLIENTE] Resposta recebida do servidor: {response_sum.result}")
    
    time.sleep(1) 

    print("\n" + "="*40)
    print(" TESTE 2: WORKLOAD (Simulação de Carga)")
    print("="*40)
    ops = 1000
    
    print(f"[CLIENTE] Pedindo para servidor processar {ops} operações...")
    response_work = stub.Workload(dist_calc_pb2.WorkloadRequest(operations=ops, payload_size=100))
    print(f"[CLIENTE] Servidor respondeu: 'Levei {response_work.time_ms:.4f} ms para processar'")

    time.sleep(1)

    print("\n" + "="*40)
    print(" TESTE 3: STREAMING (Cálculo de Média)")
    print("="*40)

    def generate_numbers():
        valores = [10, 20, 30, 40, 50]
        for i in valores:
            print(f"[CLIENTE] Enviando número via stream: {i}")
            yield dist_calc_pb2.Number(value=i)
            time.sleep(0.5) 

    print("[CLIENTE] Abrindo stream de dados...")
    response_avg = stub.StreamAverage(generate_numbers())
    print(f"[CLIENTE] Stream fechado. Resultado final: Média = {response_avg.average} (Baseado em {response_avg.count} números)")

    print("\n[CLIENTE] Demo finalizada.")

if __name__ == '__main__':
    run()