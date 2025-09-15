import { LightningElement, api } from 'lwc';
import ArgentinaFlag from '@salesforce/resourceUrl/ArgentinaFlag';
import UKFlag from '@salesforce/resourceUrl/UKFlag';
import BrazilFlag from '@salesforce/resourceUrl/BrazilFlag';

export default class LanguageSelector extends LightningElement {
    @api Seleccionar_tu_idioma; 

    argentinaSrc = ArgentinaFlag;
    ukSrc = UKFlag;
    brazilSrc = BrazilFlag;

    get isSpanishSelected() {
        return this.Seleccionar_tu_idioma === 'Spanish';
    }

    get isEnglishSelected() {
        return this.Seleccionar_tu_idioma === 'English';
    }

    get isPortugueseSelected() {
        return this.Seleccionar_tu_idioma === 'Portuguese';
    }

    handleLanguageChange(event) {
        this.Seleccionar_tu_idioma = event.target.value;

        try {
            sessionStorage.setItem('idiomaSeleccionado', this.Seleccionar_tu_idioma);
        } catch (error) {
            console.warn('SessionStorage no disponible:', error);
        }
    }
}