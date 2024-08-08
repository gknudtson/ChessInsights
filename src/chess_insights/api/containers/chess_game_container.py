from dependency_injector import containers, providers

from ... chess_board import ChessBoard


class ChessGameContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["..routes"])

    chess_board = providers.Singleton(ChessBoard)

