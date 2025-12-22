from enum import Enum
import threading

class OrderStatus(Enum):
    PLACED = "PLACED"
    CONFIRMED = "CONFIRMED"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELED = "CANCELED"



status = OrderStatus.PLACED

if status == OrderStatus.PLACED:
    print("Order has been placed.")


from abc import ABC, abstractmethod

# interface of PaymentGateway, it is an abstract base class
class PaymentGateway(ABC):
    @abstractmethod
    def initiate_payment(self, amount):
        pass

# implementation of PaymentGateway
class StripePaymentGateway(PaymentGateway):
    def initiate_payment(self, amount):
        print(f"Initiating payment of ${amount} through Stripe.")
# implementation of PaymentGateway
class PayPalPaymentGateway(PaymentGateway):
    def initiate_payment(self, amount):
        print(f"Initiating payment of ${amount} through PayPal.")


# abstraction
class Vehicle(ABC):
    def __init__(self, brand):
        self.brand = brand
    
    @abstractmethod
    def drive(self):
        pass

# inheritance
class Car(Vehicle):
    def __init__(self, brand):
        super().__init__(brand)
    
    def drive(self):
        print(f"Driving a {self.brand} car.")
    

# unidirectional association
class PaymentGateway:
    def process_payment(self, amount: float):
        pass 
class Order:
    def __init__(self, gateway: PaymentGateway):
        self.gateway = gateway

# assiociation bidirectional
class Developer:
    def __init__(self):
        self.team = None 
    
    def set_team(self, team):
        self.team = team 

class Team:
    def __init__(self):
        self.developers = []
    
    def add_developer(self, dev: Developer):
        self.developers.append(dev)
        dev.set_team(self)

# one-to-one association
class Profile:
    def __init__(self):
        self.user = None
    
    def set_user(self, user):
        self.user = user

class User:
    def __init__(self):
        self.profile = None
    
    def set_profile(self, profile):
        self.profile = profile
        profile.set_user(self)


# one-to-many association
class Issue:
    def __init__(self):
        self.project = None 
    
    def set_project(self, project):
        self.project = project

class Project:
    def __init__(self):
        self.issues = []
    
    def add_issue(self, issue: Issue):
        self.issues.append(issue)
        issue.set_project(self)


# aggregation

class Professor:
    def __init__(self, name):
        self.name = name 
    
    def get_name(self):
        return self.name 
    
class Department:
    def __init_(self, name, professors):
        self.name = name
        self.professors = professors
    
    def print_professors(self):
        print("Professors in the department:")
        for professor in self.professors:
            print(professor.get_name())

        


# Dependency, short-lived; no ownership; Uses-a relationship

class Document:
    def __init__(self, content):
        self.content = content
    
    def get_content(self):
        return self.content

class Printer:
    def print(self, document):
        print(document.get_content())

# Dependency injection
#interface
class Sender(ABC):
    @abstractmethod
    def send(self, message) -> None:
        pass 


class NotificationService:
    def __init__(self, sender: Sender):
        self.sender = sender 
    
    def notify_user(self, message):
        self.sender.send(message)



# design pattern

## Singleton pattern
class LazySingleton:
    _instance = None

    def __init__(self):
        if LazySingleton._instance is not None:
            raise Exception("This class is a singleton!")
    
    @staticmethod
    def get_instance():
        if LazySingleton._instance is None:
            LazySingleton._instance = LazySingleton()
        return LazySingleton._instance

# thread-safe Singleton pattern
class ThreadSafeSingleton:
    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        if ThreadSafeSingleton._instance is not None:
            raise Exception("This class is a singleton!")
    
    @staticmethod
    def get_instance():
        with ThreadSafeSingleton._lock:
            if ThreadSafeSingleton._instance is None:
                ThreadSafeSingleton._instance = ThreadSafeSingleton()
        return ThreadSafeSingleton._instance

# Factory pattern

class SimpleNotificationFactory:
    @staticmethod
    def create_notification(type):
        match type:
            case 'EMAIL':
                return EmailNotification()
            case 'SMS':
                return SMSNotification()
            case 'PUSH':
                return PushNotification()
            case _:
                raise ValueError("Invalid notification type")
# core logic focused. It only uses the notification, it doesn't construct it.
class NotificationService:
    def send_notification(self, type, message):
        notification = SimpleNotificationFactory.create_notification(type)
        notification.send(message)


# Factory method pattern
class Notification(ABC):
    @abstractmethod
    def send(self, message):
        pass

class EmailNotification(Notification):
    def send(self, message):
        print(f"Sending email notification with message: {message}")

class SMSNotification(Notification):
    def send(self, message):
        print(f"Sending SMS notification with message: {message}")

class PushNotification(Notification):
    def send(self, message):
        print(f"Sending push notification with message: {message}")

# Defind an abstract creator
class NotificationCreator(ABC):
    @abstractmethod
    def create_notification(self):
        pass

    def send(self, message):
        Notification = self.create_notification()
        Notification.send(message)



class EmailNotificationCreator(NotificationCreator):
    def create_notification(self):
        return EmailNotification()
    
# now I want to create slack notification
class SlackNotification(Notification):
    def send(self, message):
        print(f"Sending slack notification with message: {message}")

class SlackNotificationCreator(NotificationCreator):
    def create_notification(self):
        return SlackNotification()