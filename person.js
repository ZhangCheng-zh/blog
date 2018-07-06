import Event from'./js/eventEmitter.js';

class Person extends Event {
    constructor (name, age) {
        super(name);
        this.name = name;
        this.age = age;
        this.addHandler('message', (event) => {
            alert(event.message);
        })
    },
    say () {
        this.fire({type: 'message', message: 'This is event message'});
    }
}