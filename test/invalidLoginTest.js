const webdriver = require('selenium-webdriver');
var assert = require('assert');

const chromeDriver = require('chromedriver');
const chromeCapabilities = webdriver.Capabilities.chrome();
chromeCapabilities.set('chromeOptions', {args: ['--headless', '--disable-gpu','--no-sandbox','--disable-dev-shm-usage']});


var driver;
const timeOut = 15000;

describe(' Invalid User Authentication', function () {

    before(function() {
        this.timeout(timeOut);


        driver = new webdriver.Builder()
            .forBrowser('chrome')
            .withCapabilities(chromeCapabilities)
            .build();


    });

    beforeEach(function() {
        this.timeout(timeOut);
        driver.get("https://cse442-office-hours-app.herokuapp.com/");

    });


    it('Invalid email format', function() {
        driver.findElement(webdriver.By.name('email')).sendKeys('student86@gmail.com');
        driver.findElement(webdriver.By.name('password')).sendKeys('student86');
        driver.findElement(webdriver.By.id('log in')).click();
    });




});