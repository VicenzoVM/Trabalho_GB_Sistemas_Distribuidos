import time
import grpc
from concurrent import futures

import dist_calc_pb2
import dist_calc_pb2_grpc

class DistributedCalculatorServicer(dist_calc_pb2_grpc.DistributedCalculatorServicer):

    def Sum(self, request, context):
        print(f"\n[SERVIDOR] Recebi pedido de SOMA: {request.a} + {request.b}")
        result = request.a + request.b
        print(f"[SERVIDOR] Calculado: {result}. Enviando resposta...")
        return dist_calc_pb2.SumResponse(result=result)

    def Workload(self, request, context):
        print(f"\n[SERVIDOR] Recebi WORKLOAD: {request.operations} operações (Payload: {request.payload_size})")
        print("[SERVIDOR] Processando...", end='', flush=True)
        
        start = time.time()
        for _ in range(request.operations):
            x = 0
            for _ in range(request.payload_size):
                x += 1
        end = time.time()
        
        elapsed_ms = (end - start) * 1000
        print(f" Concluído em {elapsed_ms:.2f}ms.")
        return dist_calc_pb2.WorkloadResponse(time_ms=elapsed_ms)

    def StreamAverage(self, request_iterator, context):
        print("\n[SERVIDOR] Iniciando recebimento de STREAM para média...")
        total = 0
        count = 0

        for number in request_iterator:
            print(f"   -> [SERVIDOR] Recebido número: {number.value}")
            total += number.value
            count += 1

        average = total / count if count > 0 else 0
        print(f"[SERVIDOR] Stream finalizado. Média calculada: {average}. Retornando ao cliente.")
        return dist_calc_pb2.AverageResponse(average=average, count=count)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    dist_calc_pb2_grpc.add_DistributedCalculatorServicer_to_server(DistributedCalculatorServicer(), server)
    server.add_insecure_port('[::]:50051')
    
    print("="*40)
    print(" SERVIDOR gRPC RODANDO NA PORTA 50051")
    print(" Aguardando chamadas...")
    print("="*40)
    
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()