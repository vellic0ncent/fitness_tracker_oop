from typing import Dict, Callable, Tuple, List
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
        self.action = action
        self.duration_hrs = duration
        self.weight_kg = weight

    def get_distance(self) -> float:
        """Get distance in km."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Get mean speed in km/hr."""
        return self.get_distance() / self.duration_hrs

    def get_spent_calories(self) -> float:
        """Get spent calories."""
        raise NotImplementedError()

    def show_training_info(self) -> InfoMessage:
        """Show message about training."""
        return InfoMessage(type(self).__name__,
                           self.duration_hrs,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Training: running."""

    LEN_STEP = .65
    SPENT_CALORIE_X1: int = 18
    SPENT_CALORIE_X2: int = 20
    MINUTES_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float):
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Evaluate with special running coefficients."""
        mean_speed: float = self.get_mean_speed()
        return ((self.SPENT_CALORIE_X1 * mean_speed
                 - self.SPENT_CALORIE_X2)
                * self.weight_kg / self.M_IN_KM
                * self.duration_hrs * self.MINUTES_IN_HOUR)


class SportsWalking(Training):
    """Training: sport walking."""

    LEN_STEP = .65
    SPENT_CALORIE_X1: float = .035
    SEPNT_CALORIE_X2: float = .029
    MINUTES_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float):
        super().__init__(action, duration, weight)
        self.height_sm: float = height

    def get_spent_calories(self) -> float:
        """Evaluate with special sport walking coefficients."""
        return ((self.SPENT_CALORIE_X1 * self.weight_kg
                + (self.get_mean_speed() ** 2 // self.height_sm)
                * self.SEPNT_CALORIE_X2 * self.weight_kg)
                * self.duration_hrs * self.MINUTES_IN_HOUR)


class Swimming(Training):
    """Тренировка: плавание.

    length_pool_m — длина бассейна в метрах;
    count_pool — сколько раз пользователь переплыл бассейн.
    """
    """Training: swimming.

    Parameters
    ----------
    length_pool_m : float
        Pool length im metres.
    count_pool: int
        N of times user passed pool.
    """

    LEN_STEP: float = 1.38
    SPENT_CALORIE_X1: float = 1.1
    SPENT_CALORIE_X2: float = 2.0

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int):
        super().__init__(action, duration, weight)
        self.length_pool_m: float = length_pool
        self.count_pool: int = count_pool

    def get_spent_calories(self) -> float:
        """Evaluate calories for swimming training type."""
        mean_speed: float = self.get_mean_speed()
        return ((mean_speed + self.SPENT_CALORIE_X1)
                * self.SPENT_CALORIE_X2 * self.weight_kg)

    def get_mean_speed(self) -> float:
        """Evaluate mean speed with pool parameters."""
        return ((self.length_pool_m * self.count_pool)
                / self.M_IN_KM / self.duration_hrs)


def read_package(workout_type: str, data: list) -> Training:
    """Read the data received from the sensors."""
    workouts: Dict[str, Callable] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    return workouts[workout_type](*data)


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
