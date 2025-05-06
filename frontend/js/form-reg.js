class FormValidation {


    selectors = {
        rootElement: '[data-js-registration-form]',
        rootElementWithoutSkobki: 'data-js-registration-form'
    }

    Erormessages = {
        valueMissing: () => {
            
            return `Вы не заполнили поле`;
        },
        patternMismatch: () => {
            
            return   `Необходимо ввести: Минимум одну строчну букву. Минимум одну заглавную букву. Минимум одну цифру. `;
        },
        tooLong: () => {
            
            return `Значение слишком длинное`;
        },

        tooShort: () => {
            
            return ` Значение слишком короткое`;
        },
        
        typeMismatch: () => `Введите корректный email, например: example@mail.com`
    }



    appendText(Erormessage, target){
        const parEl = target.parentElement
        const textItem = parEl.lastElementChild
        const eror = Erormessage.join('')
        textItem.innerHTML = `<p class="erortext">${eror}</p>`
    }


    FormValidationS(target){
        const Erormessage = []
        const eror = target.validity

        Object.entries(this.Erormessages).forEach((item)=>{
            const [erorName, value] = item

            if(eror[erorName]){
                Erormessage.push(value())
            }
            

        })
        this.appendText(Erormessage, target)

        if(Erormessage.length === 0){
            return true
        } 
    }

    
    chekingBlur(target){
    

        if(target.hasAttribute('required') && target.form.hasAttribute(this.selectors.rootElementWithoutSkobki)){
            this.FormValidationS(target)
        }
    }


    chekingChange(target){
        const checkbox = target.getAttribute('type') === 'checkbox'

        if(target.hasAttribute('required') && target.form.hasAttribute(this.selectors.rootElementWithoutSkobki) && checkbox){
            this.FormValidationS(target)
        }
    }

    
    chekingSubmit(event){


        const {target} = event

        let fields = target
        fields = [...fields]
        let formcontrol = null

        for (const input of fields) {
            if(input.hasAttribute('required') && input  .form.hasAttribute(this.selectors.rootElementWithoutSkobki)){
                const bb = this.FormValidationS(input)

                if(!bb){
                    event.preventDefault()
                    if(!formcontrol){
                        formcontrol = input
                        formcontrol.focus()
                    }
                }
            }

        }
    }


    constructor(){
        this.onBlur()
        this.onChange()
        this.onSubmit()    
    }



    onBlur(){
        document.addEventListener('blur',(event)=>{
            const {target} = event

            this.chekingBlur(target)
        }, true)
    }


    onChange(){
        document.addEventListener('change',(event)=>{
            const {target} = event
            this.chekingChange(target)
        }, )
    }


    onSubmit(){
        document.addEventListener('submit', (event)=> {
            const {target} = event
            this.chekingSubmit(event)
        })
    }
}

new FormValidation()
