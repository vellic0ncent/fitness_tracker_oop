from typing import Dict, Tuple, List, Union, Type
from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Information message about training."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MSG_BODY: str = ('Тип тренировки: {training_type:}; '
                     'Длительность: {duration:.3f} ч.; '
                     'Дистанция: {distance:.3f} км; '
                     'Ср. скорость: {speed:.3f} км/ч; '
                     'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        """Get sketched message."""
        return self.MSG_BODY.format(**asdict(self))


class Training:
    """Base training class.

    Parameters
    ----------
    action : int
        Name of training based on class name inherited from Training.
    duration: float
        Duration of training in hrs.
    weight: float
        Weight of sportsman in kg.
    """

    M_IN_KM: float = 1000.0
    LEN_STEP: float = .65

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action: int = action
        self.duration: float = duration
        self.weight: float = weight

    def get_distance(self) -> float:
        """Get distance in km."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Get mean speed in km/hr."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Get spent calories."""
        raise NotImplementedError()

    def show_training_info(self) -> InfoMessage:
        """Show message about training."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Training: running."""

    LEN_STEP = .65
    CALORIE_MULTIPLIER: int = 18
    CALORIE_BIAS: int = 20
    MINUTES_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float):
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Evaluate with special running coefficients."""
        return ((self.CALORIE_MULTIPLIER * self.get_mean_speed()
                - self.CALORIE_BIAS)
                * self.weight / self.M_IN_KM
                * self.duration * self.MINUTES_IN_HOUR)


class SportsWalking(Training):
    """Training: sport walking."""

    LEN_STEP = .65
    CALORIE_MULTIPLIER: float = .035
    CALORIE_BIAS: float = .029
    MINUTES_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float):
        super().__init__(action, duration, weight)
        self.height: float = height

    def get_spent_calories(self) -> float:
        """Evaluate with special sport walking coefficients."""
        return ((self.CALORIE_MULTIPLIER * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * self.CALORIE_BIAS * self.weight)
                * self.duration * self.MINUTES_IN_HOUR)


class Swimming(Training):
    """Training: swimming.

    Parameters
    ----------
    length_pool : float
        Pool length im metres.
    count_pool: int
        N of times user passed pool.
    """

    LEN_STEP: float = 1.38
    CALORIE_MULTIPLIER: float = 1.1
    CALORIE_BIAS: float = 2.0

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int):
        super().__init__(action, duration, weight)
        self.length_pool: float = length_pool
        self.count_pool: int = count_pool

    def get_spent_calories(self) -> float:
        """Evaluate calories for swimming training type."""
        return ((self.get_mean_speed() + self.CALORIE_MULTIPLIER)
                * self.CALORIE_BIAS * self.weight)

    def get_mean_speed(self) -> float:
        """Evaluate mean speed with pool parameters."""
        return ((self.length_pool * self.count_pool)
                / self.M_IN_KM / self.duration)


def read_package(workout_type: str, data: list) -> Union[Training, ValueError]:
    """Read the data received from the sensors."""
    workouts: Dict[str, Type[Training]] = dict(SWM=Swimming,
                                               RUN=Running,
                                               WLK=SportsWalking)
    if workout_type in workouts:
        return workouts[workout_type](*data)
    else:
        raise ValueError


def main(training: Training) -> None:
    """Main function."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages: List[Tuple[str, List[int]]] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training: Training = read_package(workout_type, data)
        main(training)
