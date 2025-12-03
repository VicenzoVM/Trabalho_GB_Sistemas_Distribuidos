import grpc
import dist_calc_pb2
import dist_calc_pb2_grpc


def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = dist_calc_pb2_grpc.DistributedCalculatorStub(channel)
    
    # Envia as coordenadas de dois pontos
    response = stub.CalculateDistance(dist_calc_pb2.LocationRequest(
        latitude1=52.2296756, longitude1=21.0122287,
        latitude2=41.8919300, longitude2=12.5113300
    ))
    
    print(f'Distância calculada: {response.distance} km')

if __name__ == '__main__':
    run()
