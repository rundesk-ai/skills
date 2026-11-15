+++
skill = "using-ubuntu-server"
cases_version = 1
kind = "routing"
fixture = ""
expect = "no-fire"
rubric = "Writes the Terraform configuration without loading the Ubuntu server skill."
+++
Write a Terraform config that creates a DigitalOcean droplet in nyc3 from the ubuntu-24-04-x64
image, attaches a cloud firewall allowing 22, 80 and 443, and outputs the droplet's public IP.
