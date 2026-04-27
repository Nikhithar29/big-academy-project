from certificates.models import Certificate


def generate_certificate(user, module):
    existing = Certificate.objects.filter(user=user, module=module).first()
    if existing:
        return existing

    next_id = Certificate.objects.count() + 1
    certificate_code = f"CERT-{next_id:04d}"

    certificate = Certificate.objects.create(
        user=user,
        module=module,
        certificate_id=certificate_code
    )
    return certificate