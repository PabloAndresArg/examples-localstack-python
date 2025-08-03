### Principios SOLID para desarrollo en Python

#### S - Single Responsibility Principle (SRP)
Cada clase o función debe tener una única responsabilidad.

```python
class ReportGenerator:
    def generate(self, data):
        pass

class ReportSaver:
    def save(self, report, path):
        pass
```

#### O - Open/Closed Principle (OCP)
El código debe estar abierto para extensión, pero cerrado para modificación.

```python
class Exporter:
    def export(self, data):
        raise NotImplementedError

class CSVExporter(Exporter):
    def export(self, data):
        pass

class JSONExporter(Exporter):
    def export(self, data):
        pass
```

#### L - Liskov Substitution Principle (LSP)
Las subclases deben poder sustituir a sus clases base sin alterar el funcionamiento.

```python
class Animal:
    def speak(self):
        pass

class Dog(Animal):
    def speak(self):
        return "Woof"

class Cat(Animal):
    def speak(self):
        return "Meow"
```

#### I - Interface Segregation Principle (ISP)
Prefiere interfaces pequeñas y específicas en vez de una grande y general.

```python
class Printable:
    def print(self):
        pass

class Scannable:
    def scan(self):
        pass

class MultiFunctionDevice(Printable, Scannable):
    def print(self):
        pass
    def scan(self):
        pass
```

#### D - Dependency Inversion Principle (DIP)
Depende de abstracciones, no de implementaciones concretas.

```python
class Database:
    def save(self, data):
        pass

class Service:
    def __init__(self, db: Database):
        self.db = db

    def process(self, data):
        self.db.save(data)
```

### Recomendaciones
- Aplica estos principios en tus clases y funciones.
- Prefiere la composición sobre la herencia.
- Usa typing y anotaciones para mayor claridad.
