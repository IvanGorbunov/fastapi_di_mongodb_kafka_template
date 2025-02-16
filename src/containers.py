from dependency_injector import containers, providers

from .config import Config
from .services import GameService
from .services import KafkaService


class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(modules=[".api.routes"])

    config = providers.Configuration(yaml_files=["config.yml"])

    kafka_service_spiderweb = providers.Singleton(
        KafkaService,
        bootstrap_servers=Config.KAFKA_BOOTSTRAP_SERVERS,
        topic=Config.SPIDERWEB_TOPIC
    )

    kafka_service_nevada = providers.Singleton(
        KafkaService,
        bootstrap_servers=Config.KAFKA_BOOTSTRAP_SERVERS,
        topic="nevada.rn.operative.deferral-plan-sed"
    )

    game_service = providers.Singleton(
        GameService,
        spidey_names=Config.SPIDEY_NAMES,
        my_name=Config.MY_NAME,
        kafka_service=kafka_service_spiderweb
    )