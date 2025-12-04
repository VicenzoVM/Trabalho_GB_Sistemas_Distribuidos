import grpc
import dist_calc_pb2
import dist_calc_pb2_grpc

def run():
    channel = grpc.insecure_channel('192.168.1.14:50051')
    stub = dist_calc_pb2_grpc.DistributedCalculatorStub(channel)
    
    print("--- Teste 1: Soma Simples ---")
    response_sum = stub.Sum(dist_calc_pb2.SumRequest(a=10.5, b=20.3))
    print(f'Soma recebida: {response_sum.result}')

    print("\n--- Teste 2: Workload (Métricas para o trabalho) ---")
    response_work = stub.Workload(dist_calc_pb2.WorkloadRequest(operations=1000, payload_size=100))
    print(f'Tempo de processamento no servidor: {response_work.time_ms} ms')

    print("\n--- Teste 3: Stream Average ---")
    def generate_numbers():
        for i in [10, 20, 30, 40]:
            yield dist_calc_pb2.Number(value=i)

    response_avg = stub.StreamAverage(generate_numbers())
    print(f'Média calculada: {response_avg.average} (contagem: {response_avg.count})')

if __name__ == '__main__':
    run()