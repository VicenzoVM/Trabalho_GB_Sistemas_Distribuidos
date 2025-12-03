import time
import grpc
from concurrent import futures

import dist_calc_pb2
import dist_calc_pb2_grpc


# Implementação do serviço definido no .proto
class DistributedCalculatorServicer(dist_calc_pb2_grpc.DistributedCalculatorServicer):

    def Sum(self, request, context):
        result = request.a + request.b
        return dist_calc_pb2.SumResponse(result=result)

    def Workload(self, request, context):
        start = time.time()

        # Simula uma carga de trabalho (CPU bound)
        for _ in range(request.operations):
            x = 0
            for _ in range(request.payload_size):
                x += 1  # operação trivial só para consumir CPU

        end = time.time()
        elapsed_ms = (end - start) * 1000

        return dist_calc_pb2.WorkloadResponse(time_ms=elapsed_ms)

    def StreamAverage(self, request_iterator, context):
        total = 0
        count = 0

        for number in request_iterator:
            total += number.value
            count += 1

        average = total / count if count > 0 else 0
        return dist_calc_pb2.AverageResponse(average=average, count=count)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    dist_calc_pb2_grpc.add_DistributedCalculatorServicer_to_server(
        DistributedCalculatorServicer(), server
    )

    server.add_insecure_port('[::]:50051')
    server.start()
    print("Servidor gRPC rodando na porta 50051...")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
