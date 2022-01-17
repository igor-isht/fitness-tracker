class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        duration = format(self.duration, '.3f')
        distance = format(self.distance, '.3f')
        speed = format(self.speed, '.3f')
        calories = format(self.calories, '.3f')

        message = (f'Тип тренировки: {self.training_type}; '
                   f'Длительность: {duration} ч.; '
                   f'Дистанция: {distance} км; Ср. скорость: {speed} км/ч; '
                   f'Потрачено ккал: {calories}.')
        return message


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    MIN_IN_HOUR = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * Training.LEN_STEP / Training.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        distance = self.get_distance()
        mean_speed = distance / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info = InfoMessage(type(self).__name__, self.duration,
                           self.get_distance(),
                           self.get_mean_speed(), self.get_spent_calories())
        return info


class Running(Training):
    """Тренировка: бег."""
    COEFF_CALORIE_1 = 18
    COEFF_CALORIE_2 = 20

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        mean_speed = super().get_mean_speed()
        spent_calories = ((Running.COEFF_CALORIE_1 * mean_speed
                          - Running.COEFF_CALORIE_2)
                          * self.weight / self.M_IN_KM * self.duration
                          * Training.MIN_IN_HOUR)
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_CALORIE_1 = 0.035
    COEFF_CALORIE_2 = 2
    COEFF_CALORIE_3 = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        mean_speed = self.get_mean_speed()
        spent_calories = ((SportsWalking.COEFF_CALORIE_1 * self.weight
                          + (mean_speed**SportsWalking.COEFF_CALORIE_2
                           // self.height)
                          * SportsWalking.COEFF_CALORIE_3 * self.weight)
                          * self.duration
                          * Training.MIN_IN_HOUR)
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    COEFF_CALORIE_1 = 1.1
    COEFF_CALORIE_2 = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        distance = self.action * self.LEN_STEP / Training.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        mean_speed = (self.length_pool * self.count_pool
                      / Training.M_IN_KM / self.duration)
        return(mean_speed)

    def get_spent_calories(self) -> float:
        mean_speed = self.get_mean_speed()
        spent_calories = ((mean_speed + Swimming.COEFF_CALORIE_1)
                          * Swimming.COEFF_CALORIE_2 * self.weight)
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_types_dict = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    return training_types_dict[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
