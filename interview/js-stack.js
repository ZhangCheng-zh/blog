class Stack {
    constructor () {
        this.container = [];
    }
    push (val) {
        this.container.push(val);
        this.length = this.container.length;
    }
    pop () {
        if (this.container.length > 0) {
            let val = this.container.pop();
            this.length = this.container.length;
            return val;
        }
    }
}

