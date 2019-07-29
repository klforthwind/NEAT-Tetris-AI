class Genome {
    constructor() {
        this.inputNodes = 256;
        this.outputNodes = 7;
        this.neuralNet = [...Array(this.inputNodes).keys()].map(i => Array(this.outputNodes));
    }
}