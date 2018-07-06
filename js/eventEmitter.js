export default class Event {
    constructor () {
        this.handlers = {};
    }
    fire (event) {
        if (!event.target) {
            event.target = this;
        }
        if (this.handlers[event.type] instanceof Array) {
            let handlers = this.handlers[event.type];
            for (let i = 0, len = handlers.length; i < len; i++) {
                handlers[i](event);
            }
        }
    }
    addHandler (type, handler) {
        if (typeof type === 'string') {
            if (typeof this.handlers[type] === 'undefined') {
                this.handlers[type] = [];
            }

            this.handlers[type].push(handler);
        }
    }
    removeHandler (type, handler) {
        if (typeof type !== 'string') {
            return;
        } else {
            if (this.handlers[type] instanceof Array) {
                let handlers = this.handlers[type];
                
                for (let i = 0, len = handlers.length; i < len; i++) {
                    if (handlers[i] === handler) {
                        break;
                    }
                }

                handlers.splice(i, 1);
            }
        }
    };
}