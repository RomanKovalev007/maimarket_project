
class ModalDelteWindow{

    selectors = {
        windowDialog: '[data-js-delte-window]',
        deleteButton: '[data-js-delete-favorites]',
        windowCloseBtn: '[data-js-delte-window-close]',
        deleteProduct: '[data-js-delte-window-button]'
    }


    deletePoductFunction(target){


        this.deleteProduct.forEach((btn)=>{

            btn.addEventListener('click', ()=>{
                const closest =  target.closest('.my-products__item')
                closest.remove()
                this.dialog.close()
            })
        })
    }



    onClick(){
        this.deleteButtons.forEach((btn)=>{
            btn.addEventListener('click', (event)=>{
                this.dialog.showModal()

                const {target} = event

                this.deletePoductFunction(target)
            })
        })

        this.windowCloseBtn.forEach((btn)=>{
            btn.addEventListener('click', ()=>{
                this.dialog.close()
            })
        })

       
    }
    constructor (){
        this.dialog = document.querySelector(this.selectors.windowDialog);
        this.deleteButtons = document.querySelectorAll(this.selectors.deleteButton)
        this.windowCloseBtn =  document.querySelectorAll(this.selectors.windowCloseBtn)
        this.deleteProduct = document.querySelectorAll(this.selectors.deleteProduct)

        this.onClick()
    }
}

new ModalDelteWindow()