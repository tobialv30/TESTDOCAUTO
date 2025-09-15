import { LightningElement, api } from 'lwc';
import ArgentinaFlag from '@salesforce/resourceUrl/ArgentinaFlag';
import UKFlag from '@salesforce/resourceUrl/UKFlag';
import BrazilFlag from '@salesforce/resourceUrl/BrazilFlag';

export default class LanguageSelector extends LightningElement {
    @api Seleccionar_tu_idioma_new; 
    @api Seleccionar_tu_idioma; 

    argentinaSrc = ArgentinaFlag;
    ukSrc = UKFlag;
    brazilSrc = BrazilFlag;

    get isSpanishSelected() {
        return this.Seleccionar_tu_idioma_new === 'Spanis';
    }

    get isEnglishSelected() {
        return this.Seleccionar_tu_idioma_new === 'Engglisfghh';
    }

    get isPortugueseSelected() {
        return this.Seleccionar_tu_idioma_new === 'Portuguese';
    }

    handleLanguageChange(event) {
        this.Seleccionar_tu_idioma_new = event.target.value;

        try {
            sessionStorage.setItem('idiomaSeleccionado', this.Seleccionar_tu_idioma_new);
        } catch (error) {
            console.warn('SessionStorage no disponible:', error);
        }
    }
}