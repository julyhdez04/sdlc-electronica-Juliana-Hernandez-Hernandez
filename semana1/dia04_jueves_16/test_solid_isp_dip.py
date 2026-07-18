from semana1.dia04_jueves_16.solid_isp_dip import SensorReading, BasicTelemetrySensor, InMemoryRepository, DataProcessor, BadSensorInterface, PostgreSQLRepository

def test_basic_sensor_reading_isp() -> None:
    sensor = BasicTelemetrySensor(sensor_id="TEMP-01", value=24.5) # Instancia el sensor enfocado en lectura
    reading = sensor.read() # Obtiene la lectura empaquetada
    assert reading.sensor_id == "TEMP-01" # Valida la identidad del sensor
    assert reading.value == 24.5 # Valida el valor flotante

def test_data_processor_with_in_memory_repository_dip() -> None:
    repositorio_test = InMemoryRepository() # Crea el entorno aislado en memoria RAM sin base de datos
    procesador = DataProcessor(repository=repositorio_test) # Realiza la inyeccion de dependencias para el test
    
    lectura = SensorReading(sensor_id="HUM-02", value=60.0) # Construye los datos de prueba
    procesador.process(reading=lectura) # El procesador opera de forma transparente guardando en memoria
    
    resultado = procesador.fetch_latest(sensor_id="HUM-02") # Recupera el dato a traves de los metodos completados
    
    assert resultado is not None # Valida que la respuesta tenga contenido
    assert resultado.value == 60.0 # Valida que el dato almacenado en memoria no sufriera modificaciones
    
def test_data_processor_full_coverage():
    repo = InMemoryRepository()
    processor = DataProcessor(repo)
    reading = SensorReading("S1", 100.0)
    processor.process(reading)
    
    
    assert len(repo._storage) == 1

def test_cobertura_total_isp_dip():
    # 1. Cubrir BadSensorInterface (líneas 14, 16, 18)
    bad = BadSensorInterface()
    assert bad.read() == 0.0
    bad.write(b"data")
    bad.calibrate()
    
    # 2. Cubrir PostgreSQLRepository (líneas 68, 71)
    pg = PostgreSQLRepository()
    pg.save(SensorReading("S1", 10.0))
    assert pg.get_latest("S1") is None
